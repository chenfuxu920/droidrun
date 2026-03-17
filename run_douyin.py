import asyncio
from llama_index.llms.openai_like import OpenAILike
from droidrun import DroidAgent, AgentConfig, DroidrunConfig, FastAgentConfig, ManagerConfig, ExecutorConfig, ToolsConfig, AndroidDriver

async def main():
    llm = OpenAILike(
        model="Qwen3.5-27B",
        api_base="http://127.0.0.1:8000/v1",
        api_key="not-needed",
        is_chat_model=True,
        is_function_calling_model=True,
        additional_kwargs={
            "extra_body": {
                "top_k": 20,
                "chat_template_kwargs": {"enable_thinking": False},
            }
        },
    )

    config = DroidrunConfig(
        agent=AgentConfig(
            max_steps=5000,
            use_normalized_coordinates=True,
            fast_agent=FastAgentConfig(vision=True, codeact=False),
            manager=ManagerConfig(vision=True),
            executor=ExecutorConfig(vision=True),
            reasoning=False,
        ),
        tools=ToolsConfig(
            disabled_tools=[],
            stealth=True,
        ),
    )

    agent = DroidAgent(
        goal="""
        注意，使用视觉坐标定位，而不是控件定位！使用click_at工具，而不是click工具！
        坐标规则：屏幕坐标使用归一化坐标系统[0-1000]，左上角为(0,0)，右下角为(1000,1000)。
        例如：点击屏幕中央使用 click_at(500, 500)，点击左上角使用 click_at(0, 0)。

        抖音极速版 App 操作指南：
        - 进入 App 默认显示视频播放界面，下部中间的“赚钱”图标用于进入任务中心
        - 任务中心包含两种任务类型：看视频和看广告
        - 活动优先级：签到(显示明天领则是已参加，可以忽略)  > 开宝箱（右下角宝箱图标，图标下方显示开宝箱文字或倒计时） > 逛街赚钱  > 看视频赚金币
        - 逛街赚钱界面：右下侧有红包图标，边缘显示当前进度，此界面需持续滑动，否则任务进度会暂停，如果底部提示"暂无更多商品，再看看之前的内容吧"，则从上到下滑动，每次完成后，任务会进入冷却时间，需要返回活动中心参加其他任务
        - 看视频赚金币界面：为首页视频播放界面，右上侧有红包图标，边缘显示当前进度，此界面需持续滑动，否则任务进度会暂停，视频下方有视频进度，视频进度超过80%时，滑动播放下一个视频
        - 滑动时是从最底下滑动到最上方，滑动应该从中间快速滑动
        - 如果进入直播界面，则退出直播界面

        任务：帮我打开抖音极速版，刷金币，只参加活动优先级中提到的任务，不做下载类任务。
        """,
        llms=llm,
        config=config,
        driver=AndroidDriver(serial="2UCUT23C20006177"),
        timeout=36000,  # 增加超时到 10 小时
    )

    result = await agent.run()
    print(f"Success: {result['success']}")
    if result.get('output'):
        print(f"Output: {result['output']}")

if __name__ == "__main__":
    asyncio.run(main())
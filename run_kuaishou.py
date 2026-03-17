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

        快手极速版 App 操作指南：
        - 进入 App 默认显示视频播放界面，右下角的“去赚钱”Tab用于进入任务中心
        - 任务中心包含两种任务类型：看视频和看广告
        - 活动优先级（不参加打卡）：开宝箱（右下角宝箱图标，图标下方显示开宝箱文字或倒计时与可领取金币数）> 看视频赚金币（任务列表上部，时间达标即可） > 刷广告视频得金币（任务列表中部，每天限50次）  > 看广告得金币 （任务列表上部，无限制）
        - 注意，刷广告视频得金币和看广告得金币不一样
        - 刷广告视频得金币界面：左上侧有金钱图标，边缘显示当前进度，金钱图标下部显示已完成任务数量和总任务数量，此界面需持续滑动，否则任务进度会暂停，任务数量全部完成后点击左上角返回按钮回到任务中心
        - 看视频赚金币界面：为首页视频播放界面，右上侧有红包图标，边缘显示当前进度，此界面需持续滑动，否则任务进度会暂停，视频下方有视频进度，视频进度超过80%时，滑动播放下一个视频，给每个红心数量超过10万的视频点一下红心图标，给给每个收藏数量超过5万的视频点一下收藏图标
        - 看广告得金币界面：广告播放时左上角显示剩余时间和关闭按钮，结束后变为"已成功领取XXX金币"和"关闭"按钮，关闭后会弹出弹窗提示，点击"领取奖励"播放下一个广告，点击"弹窗右上角X图标"退出广告
        - 滑动时是从最底下滑动到最上方，滑动应该从中间下部向上部快速滑动
        - 如果进入直播界面，则观看30秒后退出直播界面

        任务：帮我打开快手极速版，刷金币，只参加活动优先级中提到的任务，不做下载类任务。
        """,
        llms=llm,
        config=config,
        driver=AndroidDriver(serial="2UCUT23C18003411"),
        timeout=36000,  # 增加超时到 10 小时
    )

    result = await agent.run()
    print(f"Success: {result['success']}")
    if result.get('output'):
        print(f"Output: {result['output']}")

if __name__ == "__main__":
    asyncio.run(main())
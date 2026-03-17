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

        汽水音乐 App 操作指南：
        - 进入 App 默认显示音乐播放界面，右上角的金钱图标用于进入福利中心
        - 福利中心包含两种奖励类型：领时长（看广告获取时长奖励）和领金币（看广告获取金币奖励）
        - 活动优先级（不参加红包雨）：签到 > 开宝箱 > 翻卡 > 逛街赚金币 > 看广告赚金币 > 连续刷视频赚金币 > 领时长
        - 常规广告播放界面（适用于签到，开宝箱，翻卡，看广告，领时长）：广告播放时右上角显示剩余时间和关闭按钮，结束后变为"继续观看"和"关闭"按钮，关闭后会弹出弹窗提示下一个广告奖励多少金币，点击"领取奖励"播放下一个广告，点击"坚持退出"退出广告
        - 逛街赚金币活动，需要持续滑动以完成广告观看，如果存在倒计时，则持续滑动，直到出现奖励领取弹窗，出现最后一个广告后，需要退出广告界面
        - 刷视频赚金币活动，同样需要持续滑动以领取，右上角出现已暂停字样时需要滑动继续观看下一个
        - 滑动时是从最底下滑动到最上方
        - 如果进入直播广告界面，则点击右上角关闭按钮退出直播广告界面
        - 宝箱活动有间隔时间要求，宝箱图标下方的倒计时就是间隔时间，可领取时是“开宝箱得金币”

        任务：帮我打开汽水音乐，打开活动奖励页，参加活动领金币，持续刷广告来领金币，如果下一个广告金币奖励少于500，则退回活动页面，参加其他活动，如果所有活动都低于500，则寻找200以上的活动参加，如果可见区域没有有效活动，则上下滑动寻找活动，直到所有奖励金币都低于100，则结束任务。
        """,
        llms=llm,
        config=config,
        driver=AndroidDriver(serial="2UCUT23C22030332"),
        timeout=36000,  # 增加超时到 10 小时
    )

    result = await agent.run()
    print(f"Success: {result['success']}")
    if result.get('output'):
        print(f"Output: {result['output']}")

if __name__ == "__main__":
    asyncio.run(main())
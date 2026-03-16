import asyncio
from llama_index.llms.openai_like import OpenAILike
from droidrun import DroidAgent, AgentConfig, DroidrunConfig, FastAgentConfig, ManagerConfig, ExecutorConfig

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
            max_steps=500,
            fast_agent=FastAgentConfig(vision=True, codeact=False),
            manager=ManagerConfig(vision=True),
            executor=ExecutorConfig(vision=True),
            reasoning=False,
        )
    )

    agent = DroidAgent(
        goal="注意，使用视觉坐标定位，而不是控件定位！使用click_at工具，而不是click工具！帮我打开汽水音乐，打开活动奖励页，参加活动持续刷广告来领金币，如果下一个广告金币奖励少于200，则退回活动页面，参加其他活动，直到所有奖励金币都低于100，则结束任务。",
        llms=llm,
        config=config,
    )

    result = await agent.run()
    print(f"Success: {result['success']}")
    if result.get('output'):
        print(f"Output: {result['output']}")

if __name__ == "__main__":
    asyncio.run(main())
import asyncio

from langchain_core.messages import HumanMessage

from graph.graph import app


async def main():
    print("Hello from untitled-folder!")
    config = {
        "configurable": {
            "thread_id": "user-1"
        }
    }
    while True:
        question=input("You: ").strip()
        if question=="quit":
            break
        response=await app.ainvoke({"question":question,"messages":[HumanMessage(content=question)]},config=config)
        print(response)
        print(f"\nAssistant: {response["generation"]}\n",end="")
    print()



if __name__ == "__main__":
    asyncio.run(main())
    app.get_graph().draw_mermaid_png(output_file_path="graph.png")

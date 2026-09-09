import asyncio

from graph.graph import app


async def main():
    print("Hello from untitled-folder!")
    while True:
        question=input("You: ").strip()
        if question=="quit":
            break
        response=await app.ainvoke({"question":question})
        print(f"\nAssistant: {response["generation"]}\n",end="")
    print()



if __name__ == "__main__":
    # asyncio.run(main())
    print(app.get_graph().draw_mermaid())

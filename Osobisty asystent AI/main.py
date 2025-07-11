from llm.local_llm import get_local_llm_chain

def main():
    print("Lokalny Asystent AI")
    conversation = get_local_llm_chain()

    while True:
        user_input = input("\nTy: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = conversation.run(user_input)
        print(f"\nAsystent:\n{response}")

if __name__ == "__main__":
    main()

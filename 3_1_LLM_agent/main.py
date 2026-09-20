# main.py

from llm_agent.core_v2 import LLMAgent


def main():
    """Демонстрация DirectoryWatcherTool"""
    print("=" * 70)
    print(" ДЕМОНСТРАЦИЯ DIRECTORY WATCHER TOOL")
    print("=" * 70)
    
    agent = LLMAgent(local=True, ollama_model="qwen3.5:0.8b")
    
    queries = [
        "Запусти отслеживание папки C:/temp",
        "Покажи статус отслеживания",
        "Покажи последние события",
        "Останови отслеживание",
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f" Запрос {i}: {query}")
        print("-" * 70)
        
        try:
            response = agent.process_query(query)
            print(f"\n💬 Ответ агента:\n{response}")
        except Exception as e:
            print(f" Ошибка: {e}")
    
    print("\n" + "=" * 70)
    print(" Демонстрация завершена!")


if __name__ == "__main__":
    main()
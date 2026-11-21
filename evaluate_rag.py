import re
import json

from app.services.rag_service import ask_question


def load_dataset():
    with open("evaluation_dataset.json", "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_rag():
    dataset = load_dataset()

    total_questions = len(dataset)
    correct_answers = 0
    correct_sources = 0

    for index, test_case in enumerate(dataset, start=1):
        print(f"\nQUESTION {index}: {test_case['question']}")

        result = ask_question(
            question=test_case["question"],
            session_id=f"evaluation_test_{index}"
        )

        actual_answer = result["answer"]
        actual_sources = result["sources"]

        print("ANSWER:", actual_answer)

        expected_page = test_case["expected_page"]

        source_found = any(
            source["filename"] == test_case["expected_source"]
            and source["page"] == expected_page
            for source in actual_sources
        )

        if source_found:
            correct_sources += 1

        # Simple keyword-based answer check
        expected_keywords = re.findall(
            r"\b\w+\b",
            test_case["expected_answer"].lower()
        )

        actual_keywords = re.findall(
            r"\b\w+\b",
            actual_answer.lower()
        )

        if all(keyword in actual_keywords for keyword in expected_keywords):
            correct_answers += 1

        print("EXPECTED PAGE:", expected_page)
        print("SOURCE FOUND:", source_found)

    print("\n========== EVALUATION RESULTS ==========")
    print(f"Total questions: {total_questions}")
    print(f"Answer accuracy: {correct_answers}/{total_questions}")
    print(f"Source accuracy: {correct_sources}/{total_questions}")


if __name__ == "__main__":
    evaluate_rag()
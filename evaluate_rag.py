
import json

from app.services.rag_service import ask_question
from app.services.llm_service import evaluate_answer


def load_dataset():
    with open("evaluation_dataset.json", "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_rag():
    dataset = load_dataset()

    total_questions = len(dataset)
    correct_answers = 0
    correct_sources = 0
    correct_abstentions = 0

    answerable_questions = 0
    unanswerable_questions = 0

    total_precision = 0
    total_recall = 0

    for index, test_case in enumerate(dataset, start=1):
        print(f"\nQUESTION {index}: {test_case['question']}")

        result = ask_question(
            question=test_case["question"],
            session_id=f"evaluation_test_{index}"
        )

        actual_answer = result["answer"]
        actual_sources = result["sources"]

        print("ANSWER:", actual_answer)

        answerable = test_case.get("answerable", True)

        answer_is_correct = evaluate_answer(
            expected_answer=test_case["expected_answer"],
            actual_answer=actual_answer
        )

        if answer_is_correct:
            correct_answers += 1

        if answerable:
            answerable_questions += 1

            expected_page = test_case["expected_page"]

            source_found = any(
                source["filename"] == test_case["expected_source"]
                and source["page"] == expected_page
                for source in actual_sources
            )

            if source_found:
                correct_sources += 1

            relevant_pages = set(test_case["relevant_pages"])

            retrieved_pages = {
                source["page"]
                for source in actual_sources
                if source["filename"] == test_case["expected_source"]
            }

            relevant_retrieved = relevant_pages.intersection(
                retrieved_pages
            )

            precision_at_3 = len(relevant_retrieved) / 3

            recall_at_3 = (
                len(relevant_retrieved) / len(relevant_pages)
                if relevant_pages else 0
            )

            total_precision += precision_at_3
            total_recall += recall_at_3

            print("EXPECTED PAGE:", expected_page)
            print("SOURCE FOUND:", source_found)
            print(f"Precision@3: {precision_at_3:.2f}")
            print(f"Recall@3: {recall_at_3:.2f}")

        else:
            unanswerable_questions += 1

            if answer_is_correct:
                correct_abstentions += 1

            print("UNANSWERABLE QUESTION: True")
            print("CORRECT ABSTENTION:", answer_is_correct)

        print("ANSWER CORRECT:", answer_is_correct)

    print("\n========== EVALUATION RESULTS ==========")
    print(f"Total questions: {total_questions}")
    print(f"Answer accuracy: {correct_answers}/{total_questions}")
    print(f"Source accuracy: {correct_sources}/{answerable_questions}")
    print(
        f"Correct abstentions: "
        f"{correct_abstentions}/{unanswerable_questions}"
    )

    if answerable_questions:
        print(
            f"Average Precision@3: "
            f"{total_precision / answerable_questions:.2%}"
        )
        print(
            f"Average Recall@3: "
            f"{total_recall / answerable_questions:.2%}"
        )


if __name__ == "__main__":
    evaluate_rag()

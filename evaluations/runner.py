from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvaluationResult:
    faithfulness: float = 0.0
    answer_relevancy: float = 0.0
    context_precision: float = 0.0
    context_recall: float = 0.0
    answer_correctness: float = 0.0
    hallucination_rate: float = 0.0
    recall_at_5: float = 0.0
    mrr: float = 0.0
    ndcg_at_10: float = 0.0
    num_test_cases: int = 0
    details: list[dict[str, Any]] = field(default_factory=list)


class EvaluationRunner:
    def __init__(self) -> None:
        pass

    async def run_ragas(
        self,
        questions: list[str],
        answers: list[str],
        contexts: list[list[str]],
    ) -> dict[str, float]:
        try:
            from ragas import evaluate
            from ragas.metrics import (
                answer_relevancy,
                context_precision,
                context_recall,
                faithfulness,
            )
            from datasets import Dataset

            data = {
                "question": questions,
                "answer": answers,
                "contexts": contexts,
            }
            dataset = Dataset.from_dict(data)
            result = evaluate(
                dataset,
                metrics=[
                    faithfulness,
                    answer_relevancy,
                    context_precision,
                    context_recall,
                ],
            )

            return {
                "faithfulness": result.get("faithfulness", 0.0),
                "answer_relevancy": result.get("answer_relevancy", 0.0),
                "context_precision": result.get("context_precision", 0.0),
                "context_recall": result.get("context_recall", 0.0),
            }
        except ImportError:
            return {
                "faithfulness": 0.0,
                "answer_relevancy": 0.0,
                "context_precision": 0.0,
                "context_recall": 0.0,
            }
        except Exception:
            return {
                "faithfulness": 0.0,
                "answer_relevancy": 0.0,
                "context_precision": 0.0,
                "context_recall": 0.0,
            }

    async def run_deepeval(
        self,
        answers: list[str],
        ground_truths: list[str],
        contexts: list[list[str]],
    ) -> dict[str, float]:
        try:
            from deepeval.metrics import AnswerCorrectnessMetric, HallucinationMetric
            from deepeval.test_case import LLMTestCase

            test_cases = [
                LLMTestCase(
                    input="",
                    actual_output=ans,
                    expected_output=gt,
                    retrieval_context=ctx,
                )
                for ans, gt, ctx in zip(answers, ground_truths, contexts)
            ]

            correctness = AnswerCorrectnessMetric()
            hallucination = HallucinationMetric()

            correctness_score = 0.0
            hallucination_score = 0.0

            if test_cases:
                correctness.measure(test_cases[0])
                correctness_score = correctness.score

                hallucination.measure(test_cases[0])
                hallucination_score = hallucination.score

            return {
                "answer_correctness": correctness_score / 100.0,
                "hallucination_rate": hallucination_score / 100.0,
            }
        except ImportError:
            return {
                "answer_correctness": 0.0,
                "hallucination_rate": 0.0,
            }
        except Exception:
            return {
                "answer_correctness": 0.0,
                "hallucination_rate": 0.0,
            }

    def compute_retrieval_metrics(
        self,
        retrieved: list[list[str]],
        relevant: list[list[str]],
        k: int = 5,
    ) -> dict[str, float]:
        recalls = []
        mrrs = []
        ndcgs = []

        for ret_docs, rel_docs in zip(retrieved, relevant):
            rel_set = set(rel_docs)

            if k <= len(ret_docs):
                retrieved_k = ret_docs[:k]
            else:
                retrieved_k = ret_docs

            hits = sum(1 for d in retrieved_k if d in rel_set)
            recalls.append(hits / max(len(rel_set), 1))

            for rank, doc in enumerate(retrieved_k, 1):
                if doc in rel_set:
                    mrrs.append(1.0 / rank)
                    break
            else:
                mrrs.append(0.0)

            dcg = sum(
                1.0 / (i + 1) for i, d in enumerate(retrieved_k) if d in rel_set
            )
            ideal = sum(1.0 / (i + 1) for i in range(min(k, len(rel_set))))
            ndcgs.append(dcg / max(ideal, 1))

        return {
            "recall_at_5": sum(recalls) / max(len(recalls), 1),
            "mrr": sum(mrrs) / max(len(mrrs), 1),
            "ndcg_at_10": sum(ndcgs) / max(len(ndcgs), 1),
        }

    async def evaluate(
        self,
        questions: list[str],
        answers: list[str],
        contexts: list[list[str]],
        ground_truths: list[str] | None = None,
        retrieved_docs: list[list[str]] | None = None,
        relevant_docs: list[list[str]] | None = None,
    ) -> EvaluationResult:
        ragas_scores = await self.run_ragas(questions, answers, contexts)

        deepeval_scores = {"answer_correctness": 0.0, "hallucination_rate": 0.0}
        if ground_truths:
            deepeval_scores = await self.run_deepeval(
                answers, ground_truths, contexts
            )

        retrieval_scores = {"recall_at_5": 0.0, "mrr": 0.0, "ndcg_at_10": 0.0}
        if retrieved_docs and relevant_docs:
            retrieval_scores = self.compute_retrieval_metrics(
                retrieved_docs, relevant_docs
            )

        return EvaluationResult(
            faithfulness=ragas_scores.get("faithfulness", 0.0),
            answer_relevancy=ragas_scores.get("answer_relevancy", 0.0),
            context_precision=ragas_scores.get("context_precision", 0.0),
            context_recall=ragas_scores.get("context_recall", 0.0),
            answer_correctness=deepeval_scores.get("answer_correctness", 0.0),
            hallucination_rate=deepeval_scores.get("hallucination_rate", 0.0),
            recall_at_5=retrieval_scores.get("recall_at_5", 0.0),
            mrr=retrieval_scores.get("mrr", 0.0),
            ndcg_at_10=retrieval_scores.get("ndcg_at_10", 0.0),
            num_test_cases=len(questions),
        )

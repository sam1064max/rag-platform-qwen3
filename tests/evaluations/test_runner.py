from evaluations.runner import EvaluationRunner


class TestEvaluationRunner:
    def test_compute_retrieval_metrics_perfect(self) -> None:
        runner = EvaluationRunner()
        retrieved = [["doc1", "doc2", "doc3", "doc4", "doc5"]]
        relevant = [["doc1", "doc3"]]
        metrics = runner.compute_retrieval_metrics(retrieved, relevant, k=5)
        assert metrics["recall_at_5"] == 1.0
        assert metrics["mrr"] == 1.0

    def test_compute_retrieval_metrics_no_match(self) -> None:
        runner = EvaluationRunner()
        retrieved = [["doc1", "doc2"]]
        relevant = [["doc3", "doc4"]]
        metrics = runner.compute_retrieval_metrics(retrieved, relevant, k=5)
        assert metrics["recall_at_5"] == 0.0
        assert metrics["mrr"] == 0.0

    def test_compute_retrieval_metrics_partial(self) -> None:
        runner = EvaluationRunner()
        retrieved = [["doc1", "doc2", "doc3"]]
        relevant = [["doc2"]]
        metrics = runner.compute_retrieval_metrics(retrieved, relevant, k=5)
        assert metrics["recall_at_5"] == 1.0
        assert metrics["mrr"] == 0.5

    def test_metric_ranges(self) -> None:
        runner = EvaluationRunner()
        metric = runner.compute_retrieval_metrics(
            [["a", "b"], ["c", "d"]],
            [["a"], ["d"]],
            k=5,
        )
        for v in metric.values():
            assert 0.0 <= v <= 1.0

    def test_empty_inputs(self) -> None:
        runner = EvaluationRunner()
        metrics = runner.compute_retrieval_metrics(
            [[]],
            [[]],
            k=5,
        )
        assert metrics["recall_at_5"] == 0.0

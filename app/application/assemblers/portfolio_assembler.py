# app\application\assemblers\portfolio_assembler.py

class PortfolioMetricsResponseAssembler:

    @staticmethod
    def build(
        request_id: str,
        params,
        engine_manifest: dict,
        engine_Correlation: dict,
        engine_IndividualMetrics: dict,
        engine_Return: dict,
        result: dict
    ) -> dict:
        return {
            "request_id": request_id,
            "engine_specification": {
                    "engine_metrics": {
                        "engine": engine_manifest["formula_version"],
                        "engine_version": engine_manifest["version"],
                        "effective_date": engine_manifest["effective_date"]
                    },
                    "engine_return": {
                        "engine": engine_Return["formula_version"],
                        "engine_version": engine_Return["version"],
                        "effective_date": engine_Return["effective_date"]
                    },
                    "engine_individual_metrics": {
                        "engine": engine_IndividualMetrics["formula_version"],
                        "engine_version": engine_IndividualMetrics["version"],
                        "effective_date": engine_IndividualMetrics["effective_date"]
                    },
                    "engine_correlation": {
                        "engine": engine_Correlation["formula_version"],
                        "engine_version": engine_Correlation["version"],
                        "effective_date": engine_Correlation["effective_date"]
                    }
                },
            "tickers": params.tickers,
            "parameters": {
                "start_date": params.start_date,
                "end_date": params.end_date
            },
            "results": result["results"]
        }

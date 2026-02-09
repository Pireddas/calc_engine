# app/application/assemblers/metrics_assembler.py

class MetricsResponseAssembler:

    @staticmethod
    def build(
        request_id: str,
        engine_manifest: dict,
        result: dict,
        ai_analysis: str
    ) -> dict:
        
        result["request_id"] = request_id
        result["engine_specification"] = {
            "engine_metrics": {
                "engine": engine_manifest["formula_version"],
                "engine_version": engine_manifest["engine_version"],
                "effective_date": engine_manifest["effective_date"]
            }
        }
        result["ai_analysis"] = ai_analysis
        return result

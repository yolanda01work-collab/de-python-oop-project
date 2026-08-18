from src.pipeline import SalesPipeline


pipeline = SalesPipeline()

summary = pipeline.run(
    dry_run=False
)

print(summary)
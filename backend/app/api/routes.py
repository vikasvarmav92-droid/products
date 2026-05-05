import csv
import io

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.session import Base, engine, get_db
from app.providers.mock.providers import MockMarketplaceProvider, MockSocialProvider, MockSupplierProvider, MockTrendsProvider
from app.schemas.opportunity import ProductOpportunityOut, ScanRequest
from app.services.scanner import OpportunityScannerService
from app.models.product_opportunity import ProductOpportunity

router = APIRouter()
Base.metadata.create_all(bind=engine)


def get_scanner() -> OpportunityScannerService:
    return OpportunityScannerService(
        trends=MockTrendsProvider(),
        social=MockSocialProvider(),
        market=MockMarketplaceProvider(),
        supplier=MockSupplierProvider(),
    )


@router.post("/scan", response_model=list[ProductOpportunityOut])
def run_scan(payload: ScanRequest, db: Session = Depends(get_db), scanner: OpportunityScannerService = Depends(get_scanner)):
    return scanner.scan(db, payload.query, payload.max_products)


@router.get("/opportunities", response_model=list[ProductOpportunityOut])
def list_opportunities(db: Session = Depends(get_db)):
    return db.query(ProductOpportunity).order_by(ProductOpportunity.final_opportunity_score.desc()).limit(200).all()


@router.get("/opportunities/export")
def export_opportunities_csv(db: Session = Depends(get_db)):
    items = db.query(ProductOpportunity).order_by(ProductOpportunity.created_at.desc()).all()
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow([
        "product_name", "supplier_url", "supplier_price_nzd", "shipping_cost_nzd", "shipping_days_estimate",
        "estimated_sell_price_nzd", "estimated_gross_margin_nzd", "demand_score", "competition_score",
        "risk_score", "final_opportunity_score", "ai_recommendation",
    ])
    for item in items:
        writer.writerow([
            item.product_name, item.supplier_url, item.supplier_price_nzd, item.shipping_cost_nzd,
            item.shipping_days_estimate, item.estimated_sell_price_nzd, item.estimated_gross_margin_nzd,
            item.demand_score, item.competition_score, item.risk_score, item.final_opportunity_score,
            item.ai_recommendation,
        ])
    stream.seek(0)
    return StreamingResponse(iter([stream.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=opportunities.csv"})

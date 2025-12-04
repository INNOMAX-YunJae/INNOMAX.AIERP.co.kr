from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required



@login_required
def dashboard(request):
    steps = [
        {
            "no": 1,
            "title": "신규 수주 → 도면/BOM 입력",
            "desc": "OCR + BOM 파서로 도면과 자재 리스트를 자동 인식",
            "status": "3건 진행 중",
        },
        {
            "no": 2,
            "title": "이전PJ 재고·트러블 분석",
            "desc": "이전 프로젝트 반입재고, 사용량 패턴, 트러블 리포트 자동 조회",
            "status": "분석 완료",
        },
        {
            "no": 3,
            "title": "부족 수량만 자동 구매요청",
            "desc": "이전PJ 재고 반영하여 불필요 구매 차단 및 누락 없이 발주 초안 생성",
            "status": "5건 생성",
        },
    ]

    context = {
        "steps": steps,
        "auto_pr_today": 5,
        "expected_overbuy_blocked": 3,
        "drawing_risk_alerts": 2,
        "knowledge_items": 1340,
    }
    return render(request, "dashboard.html", context)


@login_required
def orders_view(request):
    orders = [
        {
            "project": "프로젝트 A",
            "order_no": "A-2025-001",
            "bom_status": "도면/BOM 분석 완료",
            "auto_pr_count": 2,
            "note": "이전PJ 재고 반영 완료",
        },
        {
            "project": "프로젝트 B",
            "order_no": "B-2025-003",
            "bom_status": "분석 중",
            "auto_pr_count": 0,
            "note": "AI 분석 대기",
        },
    ]
    return render(request, "orders.html", {"orders": orders})


@login_required
def inventory_view(request):
    items = [
        {
            "code": "MAT-001",
            "name": "클램프",
            "returned_qty": 15,   # 이전PJ 반입수량
            "predicted_qty": 10,  # AI 예상 현재수량
            "note": "이전PJ 남은 자재 활용 가능",
        },
        {
            "code": "MAT-002",
            "name": "배관 피팅",
            "returned_qty": 8,
            "predicted_qty": 5,
            "note": "재고 부족 위험 낮음",
        },
    ]
    return render(request, "inventory.html", {"items": items})


@login_required
def drawings_view(request):
    drawings = [
        {
            "drawing_no": "D-1001",
            "risk_level": "높음",
            "comment": "이전PJ 누수 트러블 패턴과 유사한 CLAMP 위치 발견",
        },
        {
            "drawing_no": "D-1002",
            "risk_level": "중간",
            "comment": "이전PJ 조립 난이도 증가 패턴과 유사함",
        },
    ]
    return render(request, "drawings.html", {"drawings": drawings})


@login_required
def ai_insights_view(request):
    insights = [
        {
            "title": "이전PJ 반입재고 활용으로 과다 구매 3건 방지 예상",
            "category": "비용 절감",
            "detail": "프로젝트 A/B의 이전PJ 남은 자재를 활용하면 신규 발주 없이도 자재가 충분합니다.",
        },
        {
            "title": "도면 설계 위험 패턴 감지",
            "category": "품질 리스크",
            "detail": "이전PJ 누수 트러블 27건과 유사한 도면 패턴이 발견되었습니다. 설계 검토 권장.",
        },
    ]
    return render(request, "ai_insights.html", {"insights": insights})


def signup_view(request):
    """회원가입 + 가입 후 자동 로그인"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})

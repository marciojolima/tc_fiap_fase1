# Função de modelo fake simples
from api_books.schemas import PredictionInput, PredictionOutput


def fake_model(input: PredictionInput) -> PredictionOutput:
    """
    Modelo simulado que calcula o preço baseado em uma fórmula simples:
    - Availability: quanto maior, mais caro
    - Rating: quanto maior, mais caro
    """
    # Fórmula simples: preço base + (availability * 2) + (rating * 10)
    # Preço base de qualquer livro (R$ 25)
    base_price = 25.0
    # Estoque alto = +R$ 2 por unidade
    availability_factor = input.x1_availability * 2.0
    # Rating alto = +R$ 10 por estrela
    rating_factor = input.x2_rating * 10.0

    predicted_price = base_price + availability_factor + rating_factor

    # Simular uma confiança baseada no rating (ratings mais altos = maior confiança)
    confidence = min(0.95, max(0.6, input.x2_rating / 5.0))

    return PredictionOutput(
        predicted_price=round(predicted_price, 2), confidence=round(confidence, 2)
    )

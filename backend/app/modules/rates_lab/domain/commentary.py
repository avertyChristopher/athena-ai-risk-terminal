def bond_commentary(
    price_status: str,
    coupon_rate: float,
    yield_to_maturity: float,
    modified_duration: float | None = None,
    shock_bps: float | None = None,
    language: str = "en",
) -> dict[str, object]:
    if language == "fr":
        relations = {
            "discount": "L'obligation se negocie sous le pair puisque son rendement depasse son taux de coupon.",
            "premium": "L'obligation se negocie au-dessus du pair puisque son taux de coupon depasse son rendement.",
            "par": "L'obligation se negocie pres du pair puisque son coupon et son rendement sont alignes.",
        }
        inverse_note = "Le prix et le rendement d'une obligation evoluent en sens inverse."
        cfa_notes = [
            "Une echeance plus longue augmente generalement la sensibilite aux taux.",
            "Un coupon plus faible augmente generalement la duration, toutes choses egales par ailleurs.",
            "La convexite ameliore l'estimation lorsque les variations de rendement sont importantes.",
        ]
    else:
        relations = {
            "discount": "The bond trades below par because its yield exceeds its coupon rate.",
            "premium": "The bond trades above par because its coupon rate exceeds its yield.",
            "par": "The bond trades near par because its coupon rate and yield are aligned.",
        }
        inverse_note = "Bond prices and yields move inversely."
        cfa_notes = [
            "Longer maturities generally increase interest-rate sensitivity.",
            "Lower coupons generally increase duration, all else equal.",
            "Convexity improves estimates for larger yield changes.",
        ]

    relation = relations[price_status]
    key_points = [relation, inverse_note]
    if modified_duration is not None and shock_bps is not None:
        approximate_change = -modified_duration * shock_bps / 10_000
        if language == "fr":
            key_points.append(
                f"La duration modifiee implique une variation approximative de {approximate_change:.2%} pour le choc selectionne, avant ajustement de convexite."
            )
        else:
            key_points.append(
                f"Modified duration implies an approximate {approximate_change:.2%} price change for the selected shock before convexity."
            )
    return {
        "summary": relation,
        "key_points": key_points,
        "cfa_notes": cfa_notes,
        "not_investment_advice": True,
        "input_relationship": {
            "coupon_rate": coupon_rate,
            "yield_to_maturity": yield_to_maturity,
        },
    }


def curve_commentary(
    curve_shape: str,
    slope: float,
    language: str = "en",
) -> dict[str, object]:
    if language == "fr":
        descriptions = {
            "normal": "Les taux longs depassent les taux courts dans une courbe normalement ascendante.",
            "steep": "La courbe est pentue et integre une prime de taux long prononcee.",
            "inverted": "Les taux courts depassent les taux longs, ce qui produit une courbe inversee.",
            "flat": "Les taux courts et longs sont proches.",
        }
        key_points = [
            f"La pente de la courbe est de {slope * 10_000:.1f} points de base.",
            "Les taux forward sont implicites dans les taux spot et ne constituent pas des previsions.",
        ]
        cfa_notes = [
            "La structure par terme reflete les anticipations, les primes de risque et les conditions de marche."
        ]
    else:
        descriptions = {
            "normal": "Long-term rates exceed short-term rates in a normally upward-sloping curve.",
            "steep": "The curve is steep, with a pronounced long-term rate premium.",
            "inverted": "Short-term rates exceed long-term rates, producing an inverted curve.",
            "flat": "Short- and long-term rates are closely aligned.",
        }
        key_points = [
            f"Curve slope is {slope * 10_000:.1f} basis points.",
            "Forward rates are implied by spot rates and are not forecasts.",
        ]
        cfa_notes = [
            "The term structure reflects expectations, risk premiums and market conditions."
        ]
    return {
        "summary": descriptions[curve_shape],
        "key_points": key_points,
        "cfa_notes": cfa_notes,
        "not_investment_advice": True,
    }

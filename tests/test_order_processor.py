"""
test_order_processor.py — Tests for src/order_processor.py

Verifies that all AI-tagged functions in order_processor.py behave correctly
across happy path, edge cases, error paths, and security scenarios.
"""

import pytest
from src.order_processor import (
    Order,
    OrderError,
    OrderStatus,
    add_item,
    apply_discount,
    build_order_summary_query,
    calculate_total,
    cancel_order,
    confirm_order,
    create_order,
)


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def make_order(order_id="ORD-001", customer_id="CUST-42") -> Order:
    return create_order(order_id, customer_id)


def make_order_with_items() -> Order:
    order = make_order()
    add_item(order, "PROD-A", 2, 10.00)
    add_item(order, "PROD-B", 1, 5.50)
    return order


# ──────────────────────────────────────────────────────────────
# create_order
# ──────────────────────────────────────────────────────────────

class TestCreateOrder:
    def test_creates_order_with_correct_ids(self):
        order = create_order("ORD-001", "CUST-42")
        assert order.order_id == "ORD-001"
        assert order.customer_id == "CUST-42"

    def test_new_order_status_is_pending(self):
        order = create_order("ORD-001", "CUST-42")
        assert order.status == OrderStatus.PENDING

    def test_new_order_has_no_items(self):
        order = create_order("ORD-001", "CUST-42")
        assert order.items == []

    def test_strips_whitespace_from_ids(self):
        order = create_order("  ORD-001  ", "  CUST-42  ")
        assert order.order_id == "ORD-001"
        assert order.customer_id == "CUST-42"

    def test_empty_order_id_raises(self):
        with pytest.raises(OrderError, match="order_id cannot be empty"):
            create_order("", "CUST-42")

    def test_whitespace_only_order_id_raises(self):
        with pytest.raises(OrderError):
            create_order("   ", "CUST-42")

    def test_empty_customer_id_raises(self):
        with pytest.raises(OrderError, match="customer_id cannot be empty"):
            create_order("ORD-001", "")


# ──────────────────────────────────────────────────────────────
# add_item
# ──────────────────────────────────────────────────────────────

class TestAddItem:
    def test_adds_item_to_pending_order(self):
        order = make_order()
        add_item(order, "PROD-A", 2, 10.00)
        assert len(order.items) == 1
        assert order.items[0].product_id == "PROD-A"
        assert order.items[0].quantity == 2
        assert order.items[0].unit_price == 10.00

    def test_adds_multiple_items(self):
        order = make_order_with_items()
        assert len(order.items) == 2

    def test_returns_the_same_order(self):
        order = make_order()
        result = add_item(order, "PROD-A", 1, 5.00)
        assert result is order

    def test_cannot_add_item_to_confirmed_order(self):
        order = make_order_with_items()
        confirm_order(order)
        with pytest.raises(OrderError, match="confirmed"):
            add_item(order, "PROD-C", 1, 3.00)

    def test_cannot_add_item_to_cancelled_order(self):
        order = make_order()
        cancel_order(order)
        with pytest.raises(OrderError):
            add_item(order, "PROD-A", 1, 5.00)

    def test_zero_quantity_raises(self):
        order = make_order()
        with pytest.raises(OrderError, match="greater than zero"):
            add_item(order, "PROD-A", 0, 10.00)

    def test_negative_quantity_raises(self):
        order = make_order()
        with pytest.raises(OrderError):
            add_item(order, "PROD-A", -1, 10.00)

    def test_negative_price_raises(self):
        order = make_order()
        with pytest.raises(OrderError, match="negative"):
            add_item(order, "PROD-A", 1, -5.00)

    def test_zero_price_is_allowed(self):
        order = make_order()
        add_item(order, "FREE-ITEM", 1, 0.00)
        assert order.items[0].unit_price == 0.00

    def test_empty_product_id_raises(self):
        order = make_order()
        with pytest.raises(OrderError, match="product_id cannot be empty"):
            add_item(order, "", 1, 10.00)

    def test_bool_quantity_raises_type_error(self):
        order = make_order()
        with pytest.raises(TypeError):
            add_item(order, "PROD-A", True, 10.00)

    def test_float_quantity_raises_type_error(self):
        order = make_order()
        with pytest.raises(TypeError):
            add_item(order, "PROD-A", 1.5, 10.00)


# ──────────────────────────────────────────────────────────────
# calculate_total
# ──────────────────────────────────────────────────────────────

class TestCalculateTotal:
    def test_total_for_single_item(self):
        order = make_order()
        add_item(order, "PROD-A", 3, 10.00)
        assert calculate_total(order) == 30.00

    def test_total_for_multiple_items(self):
        order = make_order_with_items()
        # 2 * 10.00 + 1 * 5.50 = 25.50
        assert calculate_total(order) == 25.50

    def test_total_for_empty_order_is_zero(self):
        order = make_order()
        assert calculate_total(order) == 0.0

    def test_total_is_rounded_to_two_decimal_places(self):
        order = make_order()
        add_item(order, "PROD-A", 3, 0.10)  # 0.1 * 3 = 0.30000000000000004 in float
        assert calculate_total(order) == 0.30

    def test_total_with_large_quantities(self):
        order = make_order()
        add_item(order, "PROD-A", 1000, 99.99)
        assert calculate_total(order) == 99990.00


# ──────────────────────────────────────────────────────────────
# apply_discount
# ──────────────────────────────────────────────────────────────

class TestApplyDiscount:
    def test_ten_percent_discount(self):
        order = make_order_with_items()  # total = 25.50
        assert apply_discount(order, 10) == 22.95

    def test_zero_percent_discount_returns_full_total(self):
        order = make_order_with_items()
        assert apply_discount(order, 0) == 25.50

    def test_hundred_percent_discount_returns_zero(self):
        order = make_order_with_items()
        assert apply_discount(order, 100) == 0.00

    def test_discount_does_not_mutate_order(self):
        order = make_order_with_items()
        apply_discount(order, 20)
        assert calculate_total(order) == 25.50  # unchanged

    def test_negative_discount_raises(self):
        order = make_order_with_items()
        with pytest.raises(OrderError, match="between 0 and 100"):
            apply_discount(order, -10)

    def test_discount_over_100_raises(self):
        order = make_order_with_items()
        with pytest.raises(OrderError, match="between 0 and 100"):
            apply_discount(order, 101)

    def test_bool_discount_raises_type_error(self):
        order = make_order_with_items()
        with pytest.raises(TypeError):
            apply_discount(order, True)

    def test_string_discount_raises_type_error(self):
        order = make_order_with_items()
        with pytest.raises(TypeError):
            apply_discount(order, "20")


# ──────────────────────────────────────────────────────────────
# confirm_order
# ──────────────────────────────────────────────────────────────

class TestConfirmOrder:
    def test_confirms_pending_order_with_items(self):
        order = make_order_with_items()
        confirm_order(order)
        assert order.status == OrderStatus.CONFIRMED

    def test_cannot_confirm_empty_order(self):
        order = make_order()
        with pytest.raises(OrderError, match="no items"):
            confirm_order(order)

    def test_cannot_confirm_already_confirmed_order(self):
        order = make_order_with_items()
        confirm_order(order)
        with pytest.raises(OrderError, match="PENDING"):
            confirm_order(order)

    def test_cannot_confirm_cancelled_order(self):
        order = make_order_with_items()
        cancel_order(order)
        with pytest.raises(OrderError):
            confirm_order(order)


# ──────────────────────────────────────────────────────────────
# cancel_order
# ──────────────────────────────────────────────────────────────

class TestCancelOrder:
    def test_cancels_pending_order(self):
        order = make_order()
        cancel_order(order)
        assert order.status == OrderStatus.CANCELLED

    def test_cancels_confirmed_order(self):
        order = make_order_with_items()
        confirm_order(order)
        cancel_order(order)
        assert order.status == OrderStatus.CANCELLED

    def test_cannot_cancel_delivered_order(self):
        order = make_order_with_items()
        order.status = OrderStatus.DELIVERED
        with pytest.raises(OrderError, match="Delivered"):
            cancel_order(order)

    def test_cannot_cancel_already_cancelled_order(self):
        order = make_order()
        cancel_order(order)
        with pytest.raises(OrderError, match="already cancelled"):
            cancel_order(order)


# ──────────────────────────────────────────────────────────────
# build_order_summary_query
# ──────────────────────────────────────────────────────────────

class TestBuildOrderSummaryQuery:
    def test_returns_query_and_params_tuple(self):
        query, params = build_order_summary_query("ORD-001")
        assert isinstance(query, str)
        assert isinstance(params, tuple)

    def test_order_id_is_not_interpolated_into_query(self):
        query, _ = build_order_summary_query("ORD-001")
        assert "ORD-001" not in query

    def test_query_uses_placeholder(self):
        query, _ = build_order_summary_query("ORD-001")
        assert "?" in query

    def test_params_contains_order_id(self):
        _, params = build_order_summary_query("ORD-001")
        assert params == ("ORD-001",)

    def test_empty_order_id_raises(self):
        with pytest.raises(OrderError, match="order_id cannot be empty"):
            build_order_summary_query("")

    def test_whitespace_order_id_raises(self):
        with pytest.raises(OrderError):
            build_order_summary_query("   ")

    # Security edge case: SQL injection attempt goes into params, not query string
    def test_sql_injection_goes_into_params_not_query(self):
        malicious_id = "'; DROP TABLE orders;--"
        query, params = build_order_summary_query(malicious_id)
        assert "DROP TABLE" not in query
        assert params[0] == malicious_id  # safely parameterised

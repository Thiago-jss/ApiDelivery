from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from scheme import OrderSchema, ItemSchema, ResponseOrderSchema
from app.models.dependencies import get_session, verify_token
from app.models.tables import Order, User, OrderItem
from typing import List

order_router = APIRouter(
    prefix="/orders", tags=["orders"], dependencies=[Depends(verify_token)]
)


@order_router.get("/")
async def orders():
    """

    this is a placeholder for order management logic.

    """

    return {"message": "you accessed the order routes"}


@order_router.post("/order")
async def create_order(
    user_schema: OrderSchema, session: Session = Depends(get_session)
):
    new_order = Order(user_id=user_schema.user_id)
    session.add(new_order)
    session.commit()
    return {"message": f"Order successfully created. Order ID: {new_order.id}"}


@order_router.post("/order/cancel/{order_id}")
async def cancel_order(
    order_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=403,
            detail="Unfortunately, you do not have permission to make this change.",
        )
    order.status = "CANCELED"
    session.commit()
    return {
        "message": f"order number: {order.id} successfully canceled",
        "order": order,
    }


@order_router.get("/list")
async def list_all_orders(
    session: Session = Depends(get_session), user: User = Depends(verify_token)
):
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="Unfortunately, you do not have permission to make this change",
        )
    else:
        orders = session.query(Order).all()
        return {"orders": orders}


@order_router.post("/order/add-item/{order_id}")
async def add_item_order(
    order_id: int,
    item_schema: ItemSchema,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=403,
            detail="Unfortunately, you do not have permission to make this change",
        )
    order_item = OrderItem(
        item_schema.quantity,
        item_schema.flavor,
        item_schema.size,
        item_schema.unit_price,
        order_id,
    )

    session.add(order_item)
    order.calculate_price()
    session.commit()
    return {
        "message": "Item successfully created",
        "item_id": order_item.id,
        "order_price": order.price,
    }


@order_router.post("/order/remove-item/{order_item_id}")
async def remove_item_order(
    order_item_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    order_item = session.query(OrderItem).filter(OrderItem.id == order_item_id).first()

    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")

    order = session.query(Order).filter(Order.id == order_item.order_id).first()

    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=403,
            detail="Unfortunately, you do not have permission to make this change",
        )

    session.delete(order_item)
    order.calculate_price()
    session.commit()
    return {
        "message": "Item successfully removed",
        "quantity_items_ordered": len(order.items),
        "order": order,
    }


@order_router.post("/order/finish/{order_id}")
async def finish_order(
    order_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=403,
            detail="Unfortunately, you do not have permission to make this change.",
        )
    order.status = "FINISHED"
    session.commit()
    return {
        "message": f"order number: {order.id} successfully finished",
        "order": order,
    }


@order_router.get("/order/{order_id}")
async def visualize_order(
    order_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(
            status_code=403,
            detail="Unfortunately, you do not have permission to make this change.",
        )
    return {"quantity_items_ordered": len(order.items), "order": order}


@order_router.get("/list/order-user", response_model=List[ResponseOrderSchema])
async def list_orders(
    session: Session = Depends(get_session), user: User = Depends(verify_token)
):
    orders = session.query(Order).filter(Order.user_id == user.id).all()
    return orders

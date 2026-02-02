from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    status_sub: Mapped[bool] = mapped_column(default=False)
    sub_id: Mapped[int] = mapped_column(ForeignKey("subscription.id"))
    subscription: Mapped[Subscription] = relationship(back_populates="user")
    exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanges.id"))
    exchange: Mapped[Exchanges] = relationship(back_populates="user")
    statistic_id: Mapped[int] = mapped_column(ForeignKey("statistics.id"))
    statistic: Mapped[Statistics] = relationship(back_populates="user")
    order_history: Mapped[list[OrderHistory]] = relationship(back_populates="user")

class Statistics(Base):
    __tablename__ = "statistics"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[User] = relationship(back_populates="statistic")
    pnl_24_hours: Mapped[float | None] = mapped_column(nullable=True)
    pnl_7_days: Mapped[float | None] = mapped_column(nullable=True)
    pnl_30_days: Mapped[float | None] = mapped_column(nullable=True)

class Subscription(Base):
    __tablename__ = "subscription"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[User] = relationship(back_populates="subscription")
    currency: Mapped[str] = mapped_column(default="ETHUSDT")
    step_order: Mapped[float] = mapped_column(default=30)
    step_price: Mapped[float] = mapped_column(default=10)
    max_order: Mapped[int] = mapped_column(default=200)
    exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanges.id"))
    exchange: Mapped[Exchanges] = relationship(back_populates="subscription")

class Exchanges(Base):
    __tablename__ = "exchanges"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int] = mapped_column(default=1) # 1 - binance; 2 - bybit; 3 - okx, 4 - mexc
    user: Mapped[User] = relationship(back_populates="exchange")
    subscription: Mapped[Subscription] = relationship(back_populates="exchange")
    api_key: Mapped[str | None] = mapped_column(nullable=True)
    secret_key: Mapped[str | None] = mapped_column(nullable=True)
    nonce_api: Mapped[str | None] = mapped_column(nullable=True)
    nonce_secret: Mapped[str | None] = mapped_column(nullable=True)

class OrderHistory(Base):
    __tablename__ = "order_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[User] = relationship(back_populates="order_history")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    currency: Mapped[str]
    count_cur: Mapped[float]
    count_usdt: Mapped[float]
    buy_price: Mapped[float]
    commission_buy_usdt: Mapped[float]
    commission_sell_usdt: Mapped[float | None] = mapped_column(nullable=True)
    sell_price: Mapped[float | None] = mapped_column(nullable=True)
    status: Mapped[int] = mapped_column(default=1)
    pnl_usdt: Mapped[float | None] = mapped_column(nullable=True)
    date_buy: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    date_sell: Mapped[datetime | None] = mapped_column(nullable=True)





# Screaming Architecture — Quick Reference

## The 10-Second Test

Open your project's `src/` folder. Can you tell what the app does?

**YES** → You have screaming architecture.  
**NO** → You need to refactor.

## The Rule

> Package by **Feature**, not by **Layer**.

```
❌ src/                          ✅ src/
   controllers/                     orders/
   models/                          users/
   services/                        products/
   repositories/
```

## The Dependency Rule

Dependencies point **INWARD** toward the domain.

```
Presentation → Application ← Infrastructure
                    ↓
                Domain (no deps)
```

## Use Case Naming

`<Verb><Noun>UseCase`

- `PlaceOrderUseCase`
- `CancelSubscriptionUseCase`  
- `ApproveRefundUseCase`

## Framework Independence Litmus Test

Could you swap Express for Fastify by ONLY changing the `presentation/` layer?

**YES** → ✅ You're doing it right.  
**NO** → ❌ Your domain depends on framework code.

## The Golden Rule

> Zero framework imports in your domain layer.  
> Zero database imports in your domain layer.  
> Zero HTTP imports in your domain layer.

---

**Full guide (10 chapters, examples, audit):**  
→ [Screaming Architecture Field Guide ($2)](https://promptpolish-ai.github.io/screaming-architecture-guide/)

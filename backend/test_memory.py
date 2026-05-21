from memory import save_context, get_context

save_context(
    "user1",
    {
        "doctor":"Dr Sharma",
        "intent":"book"
    }
)

print(get_context("user1"))
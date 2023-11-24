import streamlit as st
import random
from googletrans import Translator


class Flashcard:
    def __init__(self, term, translation, category):
        self.term = term
        self.translation = translation
        self.category = category


if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []

if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0

if 'incorrect_answers' not in st.session_state:
    st.session_state.incorrect_answers = 0


def add_flashcard():
    term = st.text_input("Термін:", key="term_input")
    translation = st.text_input("Переклад:", key="translation_input")
    category = st.text_input("Категорія:", key="category_input")

    if term and translation and category:
        st.session_state.flashcards.append(Flashcard(term, translation, category))
        st.success("Картку додано!")


def study_flashcards():
    if not st.session_state.flashcards:
        st.warning("Додайте картку перед вивченням.")
        return

    if 'current_flashcard' not in st.session_state:
        st.session_state.current_flashcard = None

    if 'user_translation' not in st.session_state:
        st.session_state.user_translation = ""

    if 'check_answer' not in st.session_state:
        st.session_state.check_answer = False

    if not st.session_state.current_flashcard or st.session_state.check_answer:
        st.session_state.current_flashcard = random.choice(st.session_state.flashcards)
        st.session_state.check_answer = False

    user_translation = st.text_input(f"Як перекладеться '{st.session_state.current_flashcard.term}'?",
                                     key="study_input")

    if user_translation:
        st.session_state.user_translation = user_translation.lower()

    if st.button("Перевірити відповідь"):
        st.session_state.check_answer = True
        if st.session_state.user_translation == st.session_state.current_flashcard.translation.lower():
            st.session_state.correct_answers += 1
            st.success("Вірно!")
        else:
            st.session_state.incorrect_answers += 1
            st.error(f"Правильний переклад: {st.session_state.current_flashcard.translation}")

    if st.session_state.check_answer:
        st.write(f"Ваша відповідь: {st.session_state.user_translation.capitalize()}")
        st.write(f"Правильний переклад: {st.session_state.current_flashcard.translation.capitalize()}")
        st.session_state.check_answer = False

    if st.button("Наступне слово"):
        st.session_state.current_flashcard = None
        st.session_state.user_translation = ""


def view_all_flashcards():
    if not st.session_state.flashcards:
        st.warning("Додайте картку перед переглядом.")
        return

    st.header("Всі картки")
    for card in st.session_state.flashcards:
        st.write(f"**Термін:** {card.term}, Переклад: {card.translation}, Категорія: {card.category}")


def choose_category():
    categories = list(set(card.category for card in st.session_state.flashcards))
    selected_category = st.selectbox("Виберіть категорію:", ["Всі"] + categories, key="category_select")

    selected_flashcards = st.session_state.flashcards if selected_category == "Всі" else [
        card for card in st.session_state.flashcards if card.category == selected_category
    ]

    st.header(f"Картки в категорії: {selected_category}")
    for card in selected_flashcards:
        st.write(f"**Термін:** {card.term}, Переклад: {card.translation}")


def show_statistics():
    st.header("Статистика вивчення")
    total_attempts = st.session_state.correct_answers + st.session_state.incorrect_answers

    if total_attempts == 0:
        st.warning("Ще не було спроб вивчення.")
        return

    success_rate = st.session_state.correct_answers / total_attempts * 100
    st.write(f"Загальна кількість спроб: {total_attempts}")
    st.write(f"Правильних відповідей: {st.session_state.correct_answers}")
    st.write(f"Неправильних відповідей: {st.session_state.incorrect_answers}")
    st.write(f"Відсоток успішності: {success_rate:.2f}%")


def dictionary_feature():
    translator = Translator()
    german_word = st.text_input("Введите слово на немецком:")
    if german_word:
        translation_result = translator.translate(german_word, dest='uk')
        st.write(f"Переклад на українську: {translation_result.text}")


def main():
    st.title("Додаток з мовних карток")

    menu = ["Додати картку", "Вивчати картки", "Переглянути всі картки", "Вибрати картки за категорією", "Статистика вивчення", "Словник"]
    choice = st.sidebar.selectbox("Виберіть опцію", menu)

    if choice == "Додати картку":
        add_flashcard()
    elif choice == "Вивчати картки":
        study_flashcards()
    elif choice == "Переглянути всі картки":
        view_all_flashcards()
    elif choice == "Вибрати картки за категорією":
        choose_category()
    elif choice == "Статистика вивчення":
        show_statistics()
    elif choice == "Словник":
        dictionary_feature()

if __name__ == "__main__":
    main()
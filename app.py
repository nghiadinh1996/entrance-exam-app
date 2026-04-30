import re
import pandas as pd
import streamlit as st

QUESTIONS_FILE = "questions.csv"
RESULTS_FILE = "student_results.csv"

st.set_page_config(page_title="Entrance Exam", page_icon="📝", layout="centered")


def normalize_answer(text):
    text = str(text).lower().strip()
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"[.,;:!?()]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def display_number(qid):
    match = re.search(r"(\d+)$", str(qid))
    return match.group(1) if match else qid


def clean_blank_text(text):
    text = str(text)
    text = text.replace("__________", "_____")
    text = text.replace("____________", "_____")
    text = text.replace("____", "_____")
    return text.strip()


def show_reading_passage(part, section):
    if part == "Reading" and section == "Passage 1":
        st.markdown("""
### How to handle the Sun

**A.** The medical world appears to be divided on the effects of the sun upon the human body. From statements like, "There is no known relationship between a tan and health" to "perhaps sun-tanned skin absorbs the ultraviolet rays and converts them into helpful energy", there are some things which are still the topic of research. Doctors agree on one of the benefits of the sun - vitamin D. It is well known that vitamin D is acquired from the direct rays of the sun - an entirely separate miracle from sun tanning. The sun’s ultraviolet rays penetrate only a tiny amount into the human skin, but in the process, they irradiate an element in the skin called ergosterol, which is a substance that stores up reserves of vitamin D received from the sun. This is both healthy and beneficial for human skin.

**B.** Dr. W. W. Coblenz suggests that the sun cure is a major factor in the treatment of at least 23 skin diseases, ranging from acne and eczema to ulcers and wounds. Another specialist, Dr. Richard Kovacs writes, "Sun treatment is often helpful to persons suffering from general debility - repeated colds, respiratory diseases, influenza and the like". After a long winter, the return to the sun writes Dr. Leonard Dodds, the British sunlight scholar, "is a general stimulus to the body, more potent if applied after a period when it has been lacking which gradually loses its effect if exposure is over prolonged, even when not excessive".
""")

        st.markdown("""
### Question 1–4

Look at the following people and the list of statements below.

**Match each person with the correct statement.**

Write the correct letter **A–H**.

A. believes that the benefits of the sun are not scientifically provable  
B. claims to have discovered the vitamin released in the skin by the sun  
C. suggests that the sun is an excellent healer  
D. invented the first sunscreen  
E. suggests that the sun assists with common illnesses  
F. thinks that initially, the sun is of benefit to the body  
G. is unsure about the benefits of the sun  
H. thinks the location is very important in maximizing the benefit from the sun  
""")

    elif part == "Reading" and section == "Passage 2":
        st.markdown("""
### Passage 2

One of the most famous works of art in the world is Leonardo da Vinci’s Mona Lisa. Nearly everyone who goes to see the original will already be familiar with it from reproductions, but they accept that fine art is more rewardingly viewed in its original form. However, if Mona Lisa was a famous novel, few people would bother to go to a museum to read the writer’s actual manuscript rather than a printed reproduction. This might be explained by the fact that the novel has evolved precisely because of technological developments that made it possible to print out huge numbers of texts, whereas oil paintings have always been produced as unique objects. In addition, it could be argued that the practice of interpreting or "reading" each medium follows different conventions. With novels, the reader attends mainly to the meaning of words rather than the way they are printed on the page, whereas the "reader" of a painting must attend just as closely to the material form of marks and shapes in the picture as to any ideas they may signify.
""")

    elif part == "Reading" and section == "Passage 3":
        st.markdown("""
### Passage 3: Write True / False or Not Given

The practice of homeopathy was first developed by the German physician Samuel Hahnemann. During research in the 1790s, Hahnemann began experimenting with quinine, an alkaloid derived from cinchona bark that was well known at the time to have a positive effect on fever. Hahnemann started dosing himself with quinine while in a state of good health and reported in his journals that his extremities went cold, he experienced palpitations, "infinite anxiety", a trembling and weakening of the limbs, reddening cheeks, and thirst. "In short," he concluded, "all the symptoms of relapsing fever presented themselves successively..." Hahnemann’s main observation was that things which create problems for healthy people cure those problems in sick people, and this became his first principle of homeopathy: similia similibus. Hahnemann’s second principle was minimal dosing - treatments should be taken in the most diluted format which remain effective.
""")


questions = pd.read_csv(QUESTIONS_FILE).fillna("")
questions.columns = questions.columns.str.strip()

st.title("Entrance Exam")

name = st.text_input("Full name")
email = st.text_input("Email")

answers = {}
current_section = None
shown_image = False

for index, row in questions.iterrows():
    qid = str(row["question_id"]).strip()
    part = str(row["part"]).strip()
    section = str(row["section"]).strip()
    qtype = str(row["question_type"]).strip()
    question = str(row["question"]).strip()
    image = str(row.get("image", "")).strip()
    key = f"{qid}_{index}"

    section_title = f"{part} - {section}"

    if section_title != current_section:
        current_section = section_title
        st.header(section_title)
        show_reading_passage(part, section)

    if qid == "L2_14" and image and not shown_image:
        st.image(image, use_container_width=True)
        shown_image = True

    if qtype == "matching" or qid.startswith("R1_"):
        clean_name = (
            question.replace("__________", "")
            .replace("____________", "")
            .replace("_____", "")
            .replace("____", "")
            .strip()
        )

        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(f"**{display_number(qid)}. {clean_name}**")

        with col2:
            answers[qid] = st.selectbox(
                "",
                ["", "A", "B", "C", "D", "E", "F", "G", "H"],
                key=key,
                label_visibility="collapsed"
            )

    elif qtype == "multiple_choice":
        options = ["A", "B", "C", "D"]
        options = [opt for opt in options if str(row[opt]).strip() != ""]

        answers[qid] = st.radio(
            f"{display_number(qid)}. {question}",
            options,
            format_func=lambda choice, r=row: f"{choice}. {str(r[choice]).strip()}",
            key=key
        )

    elif qtype == "true_false_ng":
        answers[qid] = st.radio(
            f"{display_number(qid)}. {question}",
            ["T", "F", "NG"],
            format_func=lambda x: {
                "T": "True",
                "F": "False",
                "NG": "Not Given"
            }[x],
            key=key
        )

    else:
        if qid == "L2_11":
            st.markdown(f"**{display_number(qid)}. {clean_blank_text(question)}**")

            col1, col2 = st.columns(2)

            ans1 = col1.text_input("", key=f"{key}_1", placeholder="First word")
            ans2 = col2.text_input("", key=f"{key}_2", placeholder="Second word")

            answers[qid] = f"{ans1} {ans2}".strip()

        else:
            display_q = clean_blank_text(question)

            col1, col2 = st.columns([5, 2])

            with col1:
                st.markdown(f"**{display_number(qid)}. {display_q}**")

            with col2:
                answers[qid] = st.text_input(
                    "",
                    key=key,
                    label_visibility="collapsed"
                )

    st.write("")


submitted = st.button("Submit Exam", type="primary")

if submitted:
    if not name.strip() or not email.strip():
        st.error("Please enter both your full name and email.")
    else:
        score = 0
        total = len(questions)
        section_scores = {}
        review_rows = []

        for _, row in questions.iterrows():
            qid = str(row["question_id"]).strip()
            section_name = f"{row['part']} - {row['section']}"
            correct = str(row["correct_answer"]).strip()
            acceptable_raw = str(row["acceptable_answers"]).strip()
            student_raw = str(answers.get(qid, "")).strip()

            acceptable = [
                normalize_answer(x)
                for x in acceptable_raw.split("|")
                if x.strip()
            ]

            student_norm = normalize_answer(student_raw)
            is_correct = student_norm in acceptable

            if is_correct:
                score += 1

            if section_name not in section_scores:
                section_scores[section_name] = {"score": 0, "total": 0}

            section_scores[section_name]["total"] += 1

            if is_correct:
                section_scores[section_name]["score"] += 1

            review_rows.append({
                "Question": display_number(qid),
                "Section": section_name,
                "Your answer": student_raw,
                "Correct answer": correct,
                "Result": "Correct" if is_correct else "Incorrect"
            })

        listening_score = 0
        listening_total = 0
        reading_score = 0
        reading_total = 0

        for section_name, data in section_scores.items():
            if section_name.startswith("Listening"):
                listening_score += data["score"]
                listening_total += data["total"]
            elif section_name.startswith("Reading"):
                reading_score += data["score"]
                reading_total += data["total"]

        st.subheader("Result Summary")
        st.write(f"**{name}**")
        st.write(f"Listening score: **{listening_score}/{listening_total}**")
        st.write(f"Reading score: **{reading_score}/{reading_total}**")

        st.subheader("Answer Review")
        st.dataframe(pd.DataFrame(review_rows), use_container_width=True)

        result = pd.DataFrame([{
            "name": name,
            "email": email,
            "score": score,
            "total": total,
            "listening_score": listening_score,
            "listening_total": listening_total,
            "reading_score": reading_score,
            "reading_total": reading_total
        }])

        try:
            old_results = pd.read_csv(RESULTS_FILE)
            updated_results = pd.concat([old_results, result], ignore_index=True)
        except Exception:
            updated_results = result

        updated_results.to_csv(RESULTS_FILE, index=False)

import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="AI Resume Shortlisting",
    page_icon="📄",
    layout="wide"
)

st.title("🤖 AI Resume Shortlisting System")
st.subheader("Person 4: Email Agent + Basic Dashboard")

# -------------------------------
# SESSION STORAGE
# -------------------------------

if "candidates" not in st.session_state:
    st.session_state.candidates = []

# -------------------------------
# EMAIL AGENT
# -------------------------------

def draft_email(name, position, decision, score):

    if decision == "Shortlist":
        subject = "Congratulations! You are Shortlisted"
        message = f"""
Dear {name},

Congratulations!

You have been shortlisted for the position of {position}.

Your resume matching score is {score}%.

Our HR team will contact you regarding the next steps.

Best Regards,
HR Recruitment Team
"""

    elif decision == "Reject":
        subject = "Application Status Update"
        message = f"""
Dear {name},

Thank you for applying for the position of {position}.

After reviewing your application, we regret to inform you
that you have not been selected for the next stage.

We appreciate your interest and wish you success.

Best Regards,
HR Recruitment Team
"""

    else:
        subject = "Application Under Review"
        message = f"""
Dear {name},

Thank you for applying for the position of {position}.

Your application is currently under review.
Our HR team will update you soon.

Best Regards,
HR Recruitment Team
"""

    return subject, message


# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    ["Dashboard", "Add Candidate", "Email Agent"]
)

# -------------------------------
# DASHBOARD
# -------------------------------

if page == "Dashboard":

    st.header("📊 Recruitment Dashboard")

    candidates = st.session_state.candidates

    total = len(candidates)
    shortlisted = sum(
        c["Decision"] == "Shortlist" for c in candidates
    )
    rejected = sum(
        c["Decision"] == "Reject" for c in candidates
    )
    pending = sum(
        c["Decision"] == "Borderline" for c in candidates
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Candidates", total)
    col2.metric("Shortlisted", shortlisted)
    col3.metric("Rejected", rejected)
    col4.metric("Under Review", pending)

    st.divider()

    st.subheader("Candidate Records")

    if candidates:
        df = pd.DataFrame(candidates)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Candidate Report",
            csv,
            "candidate_report.csv",
            "text/csv"
        )
    else:
        st.info("No candidates added yet.")


# -------------------------------
# ADD CANDIDATE
# -------------------------------

elif page == "Add Candidate":

    st.header("➕ Add Candidate Details")

    with st.form("candidate_form"):

        name = st.text_input("Candidate Name")
        email = st.text_input("Candidate Email")
        position = st.text_input("Job Position")

        score = st.slider(
            "Resume Matching Score",
            0, 100, 50
        )

        decision = st.selectbox(
            "Recruitment Decision",
            ["Shortlist", "Reject", "Borderline"]
        )

        submitted = st.form_submit_button("Add Candidate")

        if submitted:

            if not name or not email or not position:
                st.error("Please fill in all the fields.")

            elif "@" not in email:
                st.error("Please enter a valid email address.")

            else:
                candidate = {
                    "Name": name,
                    "Email": email,
                    "Position": position,
                    "Score": score,
                    "Decision": decision,
                    "Date": datetime.now().strftime("%d-%m-%Y")
                }

                st.session_state.candidates.append(candidate)

                st.success("Candidate added successfully!")


# -------------------------------
# EMAIL AGENT
# -------------------------------

elif page == "Email Agent":

    st.header("📧 Automated Email Draft Generator")

    candidates = st.session_state.candidates

    if not candidates:

        st.warning("Please add a candidate first.")

    else:

        candidate_names = [
            c["Name"] for c in candidates
        ]

        selected_name = st.selectbox(
            "Select Candidate",
            candidate_names
        )

        selected_candidate = next(
            c for c in candidates
            if c["Name"] == selected_name
        )

        name = selected_candidate["Name"]
        position = selected_candidate["Position"]
        decision = selected_candidate["Decision"]
        score = selected_candidate["Score"]

        st.write("Candidate:", name)
        st.write("Position:", position)
        st.write("Decision:", decision)
        st.write("Matching Score:", f"{score}%")

        if st.button("Generate Email"):

            subject, message = draft_email(
                name,
                position,
                decision,
                score
            )

            st.session_state.email_subject = subject
            st.session_state.email_message = message

        if "email_message" in st.session_state:

            st.subheader("Generated Email")

            st.text_input(
                "Email Subject",
                value=st.session_state.email_subject
            )

            st.text_area(
                "Email Message",
                value=st.session_state.email_message,
                height=250
            )

            st.download_button(
                "Download Email Draft",
                st.session_state.email_message,
                file_name="candidate_email.txt",
                mime="text/plain"
            )

            st.caption(
                "This feature generates email drafts. "
                "It does not send emails automatically."
            )


# -------------------------------
# FOOTER
# -------------------------------

st.divider()

st.caption(
    "AI Resume Shortlisting System | "
    "Person 4 - Email Agent + Basic Dashboard"
)

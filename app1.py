import streamlit as st

def main():
    st.title("General Information Form")

    # Editable fields
    project_name = st.text_input("Project Name (as it is in the industrial license)", "ABC Company")
    location = st.text_input("Location (Region/City)", "Riyadh 1st. Industrial City")
    national_address = st.text_input("National Address", "Riyadh 1st. Industrial City")
    contact_info = st.text_input("Telephone / fax / e-mail")
    commercial_register = st.text_input("Commercial Register No. and date", "10375699376")
    industrial_license = st.text_input("Industrial license no. and date", "46659687839")
    legal_entity = st.text_input("Legal Entity", "Limited Liability Company")

    st.markdown("### Purpose of the loan")
    loan_purpose_new = st.checkbox("New Project", True)
    loan_purpose_expansion = st.checkbox("Expansion of an existing project")
    loan_purpose_modernization = st.checkbox("Modernization and development")
    loan_purpose_relocation = st.checkbox("Project relocation")
    loan_purpose_other = st.checkbox("Other (specify):")
    loan_purpose_other_text = st.text_area("If other, specify here")

    st.markdown("### Previous dealings with government financing")
    dealt_with_gov_finance = st.radio(
        "Has the project or project owners dealt previously with other government financing Funds or Credit Bank",
        options=["No", "Yes (specify):"]
    )
    gov_finance_details = st.text_area("If yes, specify here")

    st.markdown("### Previous relation with SIDF or Kafala")
    relation_with_kafala = st.radio(
        "Have the project’s owner(s) had any previous relation with SIDF or SMEs Financing Guarantee Program (Kafala)",
        options=["No", "Yes (specify):"]
    )
    kafala_details = st.text_area("If yes, specify here")

    project_completion_date = st.text_input(
        "Specify expected date for project complete implementation / Completion %",
        "1st Q 2025"
    )

    st.write("### Summary of Inputs")
    st.write({
        "Project Name": project_name,
        "Location": location,
        "National Address": national_address,
        "Contact Info": contact_info,
        "Commercial Register": commercial_register,
        "Industrial License": industrial_license,
        "Legal Entity": legal_entity,
        "Loan Purpose": {
            "New Project": loan_purpose_new,
            "Expansion": loan_purpose_expansion,
            "Modernization": loan_purpose_modernization,
            "Relocation": loan_purpose_relocation,
            "Other": loan_purpose_other,
            "Other Details": loan_purpose_other_text
        },
        "Gov Finance Dealt": dealt_with_gov_finance,
        "Gov Finance Details": gov_finance_details,
        "Kafala Relation": relation_with_kafala,
        "Kafala Details": kafala_details,
        "Project Completion Date": project_completion_date
    })

if __name__ == "__main__":
    main()

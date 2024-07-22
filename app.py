import streamlit as st

# Define the decision process
def process_flow(leak_confirm, damage_confirm, equipment_type, sub_equipment_type, low_risk, thickness_available, current_thickness, required_thickness):
    if leak_confirm == "Yes":
        return "<h4 style='font-size:14px; font-family:Tw Cen MT;'>CR-GR-HSE-426 - found at <a href='https://prgrefep.cloud.total/_layouts/15/WorkflowPage/FicheResume.aspx?idFiche=9945' target='_blank'>Reference Link</a></h4>"
    elif damage_confirm == "Yes":
        if equipment_type == "Non-pressure":
            return f"<h4 style='font-size:14px; font-family:Tw Cen MT;'>Risk assessment required</h4>"
        elif equipment_type == "Pressure":
            if low_risk:
                return "<h4 style='font-size:14px; font-family:Tw Cen MT;'>Acceptable (NC)</h4>"
            elif thickness_available:
                if current_thickness > required_thickness:
                    return "<h4 style='font-size:14px; font-family:Tw Cen MT;'>Acceptable (NC)</h4>"
                else:
                    return "<h4 style='font-size:14px; font-family:Tw Cen MT;'>Use NI Tool (NI)</h4>"
            else:
                return "<h4 style='font-size:14px; font-family:Tw Cen MT;'>Proceed with further Inspection</h4><p style='font-size:12px; font-family:Tw Cen MT;'>Detail steps based on GS-511...</p>"
    else:
        return "<h4 style='font-size:14px; font-family:Tw Cen MT;'>Follow the process by choosing some of the options on the sidebar to evaluate the NC NI workflow</h4>"

# Streamlit app
st.markdown("<h2 style='font-size:20px; font-family:Tw Cen MT;'>NI Decision Process</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='font-size:18px; font-family:Tw Cen MT;'>Inspection Visual + NDT</h3>", unsafe_allow_html=True)
inspection_options = st.sidebar.multiselect("Select options:", ["Leak", "Damage"])

leak_confirm = None
damage_confirm = None
equipment_type = None
sub_equipment_type = None
low_risk = None
thickness_available = None
current_thickness = None
required_thickness = None

if "Leak" in inspection_options:
    leak_confirm = st.sidebar.radio("Leak?", ["Yes", "No"])

if "Damage" in inspection_options:
    damage_confirm = st.sidebar.radio("Damage?", ["Yes", "No"], disabled=(leak_confirm == "Yes"))

    if damage_confirm == "Yes":
        equipment_type = st.sidebar.selectbox("Equipment Type", ["Non-pressure", "Pressure"], disabled=(leak_confirm == "Yes"))
        if equipment_type == "Non-pressure":
            sub_equipment_type = st.sidebar.selectbox("Sub-Equipment Type", ["Jacket", "Lifting heavy", "Lifting secondary", "Main beam-col"], disabled=(leak_confirm == "Yes"))
        elif equipment_type == "Pressure":
            low_risk = st.sidebar.radio("Low Risk Fluid and No Rupture?", ["Yes", "No"])
            if low_risk == "No":
                thickness_available = st.sidebar.radio("Thickness Available?", ["Yes", "No"])
                if thickness_available == "Yes":
                    current_thickness = st.sidebar.number_input("Current Measured Thickness (mm)", min_value=0.0)
                    required_thickness = st.sidebar.number_input("Thickness Required Before Next Inspection (mm)", min_value=0.0)

# Process the inputs and display the result
result = process_flow(leak_confirm, damage_confirm, equipment_type, sub_equipment_type, low_risk, thickness_available, current_thickness, required_thickness)
st.markdown(f"<div style='font-size:16px; font-family:Tw Cen MT;'>Decision process workflow: {result}</div>", unsafe_allow_html=True)

# Chat input streamer - commented out
# st.markdown("<h3>Chat Input</h3>", unsafe_allow_html=True)
# user_input = st.text_input("Enter your query or input:")

# Display the chat input - commented out
# if user_input:
#     st.write(f"You entered: {user_input}")

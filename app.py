import streamlit as st
 
# Define the decision process
def process_flow(leak, damage, equipment_type, sub_equipment_type, low_risk, thickness_available, acceptable_remaining_life, not_acceptable_remaining_life):
    if leak:
       return "CR-GR-HSE-426 - found at https://prgrefep.cloud.total/_layouts' target='_blank'>Reference Link</a></h4>"
    elif damage:
        if equipment_type == "Non-pressure":
            return f"<h4 style='font-size:14px; font-family:Tw Cen MT;'>Risk assessment required</h4>"
        elif equipment_type == "Pressure":
            if low_risk:
                return "<h4 style='font-size:14px; font-family:Tw Cen MT;'>Acceptable (NC)</h4>"
            elif thickness_available:
                if acceptable_remaining_life:
                    return "<h4 style='font-size:14px; font-family:Tw Cen MT;'>Acceptable (NC)</h4>"
                elif not_acceptable_remaining_life:
                    return "<h4 style='font-size:14px; font-family:Tw Cen MT;'>Use NI Tool (NI)</h4>"
            else:
                return "<h4 style='font-size:14px; font-family:Tw Cen MT;'>Proceed with further Inspection</h4><p style='font-size:12px; font-family:Tw Cen MT;'>Detail steps based on GS-511...</p>"
    else:
        return "<h4 style='font-size:14px; font-family:Tw Cen MT;'>Generate Inspection Report</h4>"
 
# Streamlit app
st.markdown("<h2 style='font-size:20px; font-family:Tw Cen MT;'>NI Decision Process</h2>", unsafe_allow_html=True)
 
st.sidebar.markdown("<h3 style='font-size:18px; font-family:Tw Cen MT;'>Inspection Inputs</h3>", unsafe_allow_html=True)
leak = st.sidebar.checkbox("Leak?")
damage = st.sidebar.checkbox("Damage?", disabled=leak)
 
equipment_type = None
sub_equipment_type = None
 
if damage and not leak:
    equipment_type = st.sidebar.selectbox("Equipment Type", ["Non-pressure", "Pressure"], disabled=leak)
    if equipment_type == "Non-pressure":
        sub_equipment_type = st.sidebar.selectbox("Sub-Equipment Type", ["Jacket", "Lifting heavy", "Lifting secondary", "Main beam-col"], disabled=leak)
 
low_risk = st.sidebar.checkbox("Low Risk Fluid and No Rupture?") if damage and equipment_type == "Pressure" and not leak else False
thickness_available = st.sidebar.checkbox("Thickness Available?") if damage and equipment_type == "Pressure" and not low_risk and not leak else False
 
acceptable_remaining_life = st.sidebar.checkbox("Acceptable Remaining Life (T > T_req before next inspection)?", disabled=not thickness_available or not damage or not equipment_type == "Pressure" or leak)
not_acceptable_remaining_life = st.sidebar.checkbox("Not Acceptable Remaining Life (T < T_req before next inspection)?", disabled=not thickness_available or not damage or not equipment_type == "Pressure" or leak or acceptable_remaining_life)
 
# Process the inputs and display the result
result = process_flow(leak, damage, equipment_type, sub_equipment_type, low_risk, thickness_available, acceptable_remaining_life, not_acceptable_remaining_life)
st.markdown(f"<div style='font-size:16px; font-family:Tw Cen MT;'>Decision: {result}</div>", unsafe_allow_html=True)
 
# Chat input streamer - commented out
# st.markdown("<h3>Chat Input</h3>", unsafe_allow_html=True)
# user_input = st.text_input("Enter your query or input:")
 
# Display the chat input - commented out
# if user_input:
#     st.write(f"You entered: {user_input}")

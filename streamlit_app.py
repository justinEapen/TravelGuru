import cohere
import streamlit as st

co = cohere.Client('18V1Oo06GAf0xMaXbBjkHlhdHktqbjc5tusZHZMV')  # Replace with your actual API key

st.set_page_config(page_title="Smart Travel Planner")
st.title("Your Personalized Travel Itinerary")

preamble_prompt = """
You are a Smart Travel Planner AI. Your goal is to create a detailed travel itinerary based on the User's destination, dates, and preferences.
Ask the User for their destination, travel dates, number of days, preferred travel style (adventure, leisure, cultural, etc.), and any specific interests (historical sites, food, nature, etc.).
Then, generate a well-structured day-wise travel plan with recommended places to visit, activities, and dining options.
Also, provide estimated travel times, local transportation recommendations, and any essential travel tips.
"""

def cohereReply(prompt):
    response = co.chat(
        message=prompt,
        model='command-r-plus',
        preamble=preamble_prompt,
        chat_history=st.session_state.messages,
        connectors=[{"id": "web-search"}],
    )
    return response.text

def initialize_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    initialize_state()

    st.write("Plan your perfect trip effortlessly! Enter your details below.")
    
    destination = st.text_input("Enter your destination:")
    start_date = st.date_input("Start date:")
    days = st.number_input("Number of days:", min_value=1, step=1)
    travel_style = st.selectbox("Preferred travel style:", ["Adventure", "Leisure", "Cultural", "Food & Wine", "Nature & Wildlife", "Mixed"])
    interests = st.text_area("Any specific interests? (e.g., historical sites, beaches, hiking)")
    
    if st.button("Generate Itinerary"):
        if destination and start_date and days:
            user_prompt = (f"Create a detailed {days}-day travel itinerary for {destination} starting from {start_date}. "
                           f"The travel style is {travel_style}. Interests include: {interests}.")
            
            response = cohereReply(user_prompt)
            
            with st.expander("Your Travel Itinerary:"):
                st.markdown(response)
            
            st.session_state.messages.append({"role": "User", "message": user_prompt})
            st.session_state.messages.append({"role": "Chatbot", "message": response})
        else:
            st.warning("Please fill in all required fields.")

if __name__ == "__main__":
    main()

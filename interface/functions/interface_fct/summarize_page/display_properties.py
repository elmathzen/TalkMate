import streamlit as st


def display_options(lang):
    if 'info_visible' not in st.session_state:
        st.session_state.info_visible = False

    max_length = st.sidebar.slider("Longueur maximale du résumé" if lang == "Fr" else "Maximum Length of summary",
                                   min_value=50, max_value=300, value=100, step=10)
    min_length = st.sidebar.slider("Longueur minimale du résumé" if lang == "Fr" else "Minimum Length of summary",
                                   min_value=5, max_value=100, value=30, step=5)

    st.sidebar.markdown("<hr style='margin:2px;'>", unsafe_allow_html=True)

    batch_size = st.sidebar.number_input("Taille du lot" if lang == "Fr" else "Batch size",
                                         min_value=2, max_value=16, step=1, value=4)

    st.sidebar.markdown("<hr style='margin:2px;'>", unsafe_allow_html=True)

    top_k = st.sidebar.slider("top_k", min_value=5, max_value=200, value=10, step=5)

    top_p = st.sidebar.number_input("top_p", min_value=0.1, max_value=1.0, step=0.1, value=0.4)

    # Button to toggle info
    if st.sidebar.button("Info"):
        st.session_state.info_visible = not st.session_state.info_visible

    # Show informations if info_visible is True
    if st.session_state.info_visible:
        # Information about top_k
        st.sidebar.info(
            "Le paramètre top_k contrôle le nombre de mots les plus probables utilisés dans la génération de texte. "
            "Augmenter cette valeur diversifie le texte mais diminue sa cohérence. Des valeurs plus élevées produisent "
            "des résultats plus variés mais moins précis."
            if lang == "Fr" else 
            "The top_k parameter controls the number of most likely words used in text generation. "
            "Increasing this value diversifies the text but decreases its coherence. Higher values produce "
            "more varied but less precise results."
        )

        # Information about top_p
        st.sidebar.info(
            "Le paramètre top_p, appelé aussi nucleus sampling, détermine un seuil de probabilité "
            "pour les tokens dans l'échantillonnage. En augmentant ce seuil, le modèle explore plus "
            "de choix, augmentant la diversité du texte généré. Cependant, une valeur plus élevée peut "
            "diminuer la qualité et la cohérence du texte en sélectionnant des tokens moins probables."
            if lang == "Fr" else 
            "The top_p parameter, also called nucleus sampling, determines a probability threshold"
            "for tokens in the sample. By increasing this threshold, the model explores more"
            "of choice, increasing the diversity of the generated text. However, a higher value may "
            "decrease the quality and consistency of the text by selecting less likely tokens."
        )
    return max_length, min_length, batch_size, top_k, top_p
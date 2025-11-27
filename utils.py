import streamlit as st

def inject_custom_css():
    """Inject custom CSS for styling and dark mode support."""
    st.markdown(
        """
        <style>
        /* Global Styles - Dark Blue Theme */
        .stApp {
            background-color: #001F3F; /* Dark Blue */
            color: #FFFFFF;
        }
        
        /* Title Style - Bright White */
        .custom-title {
            font-size: 1.8rem !important;
            font-weight: bold;
            text-align: center;
            margin-bottom: 1rem;
            color: #FFFFFF !important; /* Force White */
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        }

        /* Widget Labels (Date Input, Text Area, etc.) */
        .stDateInput label, .stTextArea label, .stSelectbox label, .stTextInput label {
            color: #FFFFFF !important;
            font-weight: bold;
            font-size: 1.2rem !important; /* Increased font size */
        }
        
        /* Buttons */
        .stButton button {
            color: #000000 !important; /* Black text for visibility */
            background-color: #FFFFFF !important; /* White background */
            border: none;
            font-weight: bold;
            font-size: 1.2rem !important; /* Increased font size */
        }
        .stButton button:hover {
            background-color: #E0E0E0 !important;
            color: #000000 !important;
        }

        /* Card/Container Style */
        .news-card {
            padding: 1.5rem;
            border-radius: 10px;
            background-color: #003366; /* Slightly lighter blue for cards */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem;
            border: 1px solid #004080;
        }
        
        /* Text Colors in Card */
        .news-card h3 {
            color: #FFFFFF !important;
        }
        .news-card p {
            color: #E0E0E0 !important;
        }

        /* Mobile Optimization */
        @media (max-width: 768px) {
            .stButton button {
                width: 100%;
            }
        }
        
        /* Status Message Area (Normal Flow) */
        .status-area {
            margin-top: 10px;
            margin-bottom: 20px;
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            text-align: center;
            color: #FFFFFF;
            font-size: 1.2rem !important; /* Increased font size */
            font-weight: bold;
        }
        
        /* Adjust Update Button Alignment */
        div[data-testid="column"] button {
            margin-top: 0px; 
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def inject_swipe_detection():
    """
    Inject JavaScript to detect swipe gestures and trigger keyboard events.
    Also listens for Arrow keys for Desktop navigation.
    Includes logic to HIDE the navigation buttons.
    """
    st.components.v1.html(
        """
        <script>
        // === Swipe & Keyboard Logic ===
        document.addEventListener('touchstart', handleTouchStart, false);
        document.addEventListener('touchmove', handleTouchMove, false);
        document.addEventListener('keydown', handleKeyDown, false);

        var xDown = null;                                                        
        var yDown = null;

        function handleTouchStart(evt) {
            const firstTouch = evt.touches[0];                                      
            xDown = firstTouch.clientX;                                      
            yDown = firstTouch.clientY;                                      
        };                                                

        function handleTouchMove(evt) {
            if ( ! xDown || ! yDown ) {
                return;
            }

            var xUp = evt.touches[0].clientX;                                    
            var yUp = evt.touches[0].clientY;

            var xDiff = xDown - xUp;
            var yDiff = yDown - yUp;

            if ( Math.abs( xDiff ) > Math.abs( yDiff ) ) {/*most significant*/
                if ( xDiff > 0 ) {
                    /* right swipe -> next */
                    sendMessageToStreamlit('next');
                } else {
                    /* left swipe -> prev */
                    sendMessageToStreamlit('prev');
                }                       
            }
            /* reset values */
            xDown = null;
            yDown = null;                                             
        };
        
        function handleKeyDown(e) {
            if (e.key === "ArrowRight") {
                sendMessageToStreamlit('next');
            } else if (e.key === "ArrowLeft") {
                sendMessageToStreamlit('prev');
            }
        }

        function sendMessageToStreamlit(action) {
            const buttons = window.parent.document.querySelectorAll('button');
            buttons.forEach(btn => {
                if (action === 'next' && (btn.innerText.includes("NextHidden") || btn.innerText.includes("下一則"))) {
                    btn.click();
                }
                if (action === 'prev' && (btn.innerText.includes("PrevHidden") || btn.innerText.includes("上一則"))) {
                    btn.click();
                }
            });
        }
        
        // === Hide Buttons Logic (Robust) ===
        function hideButtons() {
            const buttons = window.parent.document.querySelectorAll('button');
            buttons.forEach(btn => {
                if (btn.innerText.includes("NextHidden") || btn.innerText.includes("PrevHidden")) {
                    // Hide the button container (usually the parent div of the button)
                    // or just the button itself.
                    btn.style.display = 'none';
                    // Also try to hide the parent column if it's the only thing there? 
                    // No, that might be risky. Just hiding the button is enough.
                }
            });
        }
        
        // Run immediately and periodically to catch re-renders
        hideButtons();
        setInterval(hideButtons, 500);
        </script>
        """,
        height=0,
    )

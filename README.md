# Bot Trade
###### by kuisskui

Create and Run new **Strategy**, they place new trade for **Bots** to follow trade.

This document provides documents for creating new strategies and interfaces, including APIs for states of objects.

---

## Installation

### Pre Requirements
- Python >= 3.12.4
- Window OS

### Step
1. Clone Repository.
    ```
    git clone https://github.com/kuisskui/bot_trade.git
    ```
2. Change directory to the project.
    ```
    cd bot_trade
    ```
3. Create virtual environment (and activate).
    ```
    python -m venv venv
    ```
4. Install dependencies.
    ```
    pip install -r requirements.txt
    ```
5. Change file name **.env.example** file name to **.env** in base directory.
6. Set some configs in .env file.
    ```
    BASE_DIR=<to base directory of project (ex. C:\Users\bot_trade)>
    ```
7. Open and login Metatrader 5.
8. Start the application.
    ```
    uvicorn main:app
    ```

## Strategy Interface
1. Use for collecting state of strategy.
    ```
    get_state() # the state that you want to use or store.
    ```
2. Use for keep all state through lifetime.
    ```
    update_state(current_state, new_state)
   
    current_state: dict
    new_state: dict
    return: dict
    ```

3. Use for end the one cycle of the script.
    ```
    end(state)
   
    state: dict # the state that you want to keep through the lifetime.
    return: void
    ```

## API

## Development Collaborative Project Goals
### User cases
- Dynamic creation of new strategies.
- Run strategies with optional parameters.
- Users can follow strategies and trade according to output of strategy.

### Optional 
- Frontend for display realtime states.
- Visual states and graphs of strategies.
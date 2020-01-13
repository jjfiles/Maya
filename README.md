# Maya
Multifuctional Discord Bot

# Schedule Cog 
- whereis "NAME" command. 
    - Searches for a sheet with the name given. Gives data from cell containing weekday and hour
        - Input
        ```sh
        ~whereis Jeff
        ```
        - Output
        ```sh
        Work
        ```

- free "NAME" command.
    - Searches sheet with given name. Checks for any available free time give for remainder of day
        - Input
        ```sh
        free Jeff
        ```
        - Output
        ```sh
        Jeff is free from 18:00-20:00, and 22:00-00:00
        ```

## Hidden files 
# Secrets.py
- in root dir
    - Required
    ```sh
    token = "YOUR DISCORD BOT TOKEN"
    ```
    - If using Schedule cog
    ```sh
    spreadid = "YOUR SPREADSHEET ID"
    ```
# credentials.json
- required only if using schedule cog
    - recieved from this link: https://developers.google.com/sheets/api/quickstart/python
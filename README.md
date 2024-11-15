Anime Recommendation System based on your My Anime List Profile. Uses custom imlpementation of a low rank approximation algorithm. 

Check it out at https://animerec.net 

Full Stack Diagram: 
```mermaid

%%{init: {'theme': 'base', 'themeVariables': { 'background': '#ffffff' }}}%%
flowchart TD
    User((User))
    Frontend[Web Interface]
    Backend[Backend Server]
    API[Anime API]
    DB[(Database)]
    
    %% Data Processing nodes
    Clean[Data Cleanup]
    Matrix[Matrix Approximation]
    Match[Recommendation Matching]

    subgraph Client ["Client Side"]
        User
        Frontend
    end
    
    subgraph Server ["Server Side"]
        Backend
        subgraph Processing ["Data Processing"]
            Clean
            Matrix
            Match
        end
        DB
    end
    
    subgraph External ["External Services"]
        API
    end

    %% Main flow
    User -->|1. Request| Frontend
    Frontend -->|2. Send Preferences| Backend
    Backend -->|3. Query| API
    API -->|4. Return Anime Data| Backend
    
    %% Processing flow
    Backend -->|5. Raw Data| Clean
    Clean -->|6. Clean Data| Matrix
    Matrix -->|7. User-Anime Matrix| Match
    Match -->|8. Get Similar Users| DB
    DB -->|9. User History| Match
    Match -->|10. Top Matches| Backend
    
    Backend -->|11. Store Results| DB
    Backend -->|12. Send Recommendations| Frontend
    Frontend -->|13. Display| User

    classDef default fill:#ffffff,stroke:#333,stroke-width:2px
    classDef client fill:#e1f5fe,stroke:#333,stroke-width:2px
    classDef server fill:#fff3e0,stroke:#333,stroke-width:2px
    classDef external fill:#e8f5e9,stroke:#333,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#333,stroke-width:2px

    class User,Frontend client
    class Backend,DB server
    class API external
    class Clean,Matrix,Match process


    ```

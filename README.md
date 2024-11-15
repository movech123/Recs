Anime Recommendation System based on your My Anime List Profile. Uses custom imlpementation of a low rank approximation algorithm. 

Check it out at https://animerec.net 

Full Stack Diagram: 
```mermaid


flowchart TD
    User((User))
    Frontend[Web Interface]
    Backend[Backend Server]
    API[Anime API]
    DB[(Database)]
    
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

    User --> Frontend
    Frontend --> Backend
    Backend --> API
    API --> Backend
    
    Backend --> Clean
    Clean --> Matrix
    Matrix --> Match
    Match --> DB
    DB --> Match
    Match --> Backend
    
    Backend --> DB
    Backend --> Frontend
    Frontend --> User

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

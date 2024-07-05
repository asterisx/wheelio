## Features
- [x] Each service has independence in terms of its data, through a separate node for the database (for scalability and reliability), but the schema owner is the service.
- [x] Synchronization of schemas and models shared across services can be achieved by using gRPC or API Schemas.
- [x] For this coding challenge, gRPC is not used; instead, there are repeated fields in a few places.
- [x] The notification service is currently not saving notifications, which can be implemented easily but is not part of the requirements.
- [x] For internal API calls, Consul is being used.
- [x] Docker is used for setting up services and inter-service communication via docker-compose. For production, Kubernetes with a service discovery mechanism and safer environment variable injection through CI/CD pipelines would be used.
- [x] Statuses are in the user service but are fetched from the network_service for independence and scalability. You will see services working together to deliver data.
- [x] Shared packages are shared locally, but versioning is missing. Versioning is important in a microservice architecture to avoid breaking changes and to upgrade/downgrade packages without breaking services.
- [x] Inter-microservice communication should ideally be done with gRPC with mTLS (if security is a concern) and not with HTTP calls.
- [x] RabbitMQ is used for event management and SSE is synced up with RabbitMQ to send notifications. This allows domain separation of concerns which is an important implementation detail.
- [x] A FastAPI proxy sits in front of all the services which manages session management. This is not the best implementation; a more suitable solution would be using Nginx or something else to direct backward requests forwards. However, for a coding assessment, it is fine.

## Further Improvements
- [x] Multiple docker-compose files, using extend to make it just about digetable. Right now it's a quick and dirty implementation.
- [x] Implement a more robust service health check.
- [x] Implement versioning.
- [x] Use aliases for packages and local package management.
- [x] Augment service discovery with OpenAPI standards for internal use.
- [x] Implement graceful error handling for improved reporting.
- [x] Improve robustness, reliability, and fail-safe mechanisms across services.

## Choices
- Inter-service communication is done via HTTP calls for this coding challenge for quicker implementation.
- Docker-compose is used for setting up services and inter-service communication.
- Shared packages are built locally without versioning.
- Internal service discovery and hardening is flaky at the moment, using headers to do this. Hardening is a large topic but the general idea is never to assume your code will always run in a safe and closed environment. However, hardening is beyond the topic of this coding challenge.
- Redux toolkit was used for quick prototyping and quickly generating the API code. It's a bit messy but the choice was made out of the need for speed.

## Why microservice architecture?

- Microservices allow independent deployment and scaling of services, which is crucial for handling user interactions like friend requests and status updates and distinct notifications.
- If you look at the domains: social network (send friend request, accept friend request, block users, report users), they seem like a domain of actions on a network.
- Then there are user actions which right now are statuses but as any app will grow so will complexity.
- And then we have notifications. The notifications do not fit the bill of core code, it's important but in a different way, thus it's like a concern of its own. If you look at the architecture that is how I have structured the services.
- And with MS, we can scale up based on the consumption of the domains.
- The architecture supports fault isolation, so issues in one service do not affect the entire application, enhancing reliability.
- So, the choice was made with an understanding of how an app like this grows and how domains become concerns of their own.

## Issues
- Notifications as of now are a hit and miss.

## Build Instructions

- Run `docker-compose up --build` to build and start the services.

## Documentation

- Documentation is available via Swagger at `http://localhost:8000/docs` once docker-compose finishes,
frontend is serviced at `http://localhost:3000`.

## Full Stack Developer Technical Assignment

### Technologies

- [x] Python
- [x] TypeScript
- [x] React
- Optional: ~~WebSocket~~ For the current functionality as per the spec, SSE is a better solution than WebSocket, particularly when it comes to the topics of security.

### Objective

Develop a "Friend Connection" application that allows users to connect with friends, send and receive friend requests, and get live updates on friends' statuses.

### Time Spent

It took me 12 hours to build this.

### User Journeys

- [x] New user:
  - [x] A user, Bob, lands on a main page where he finds a list of all users on the platform.
  - [x] Bob joins by adding either a unique username or email.
  - [x] Bob selects another user, Alice, and a page or modal renders to show Alice’s profile with her status and a button to send her a friend request.
- [x] Invitee:
  - [x] Alice receives a notification of a friend request.
  - [x] Alice can either accept or reject the request.
  - [x] Alice accepts the request.
  - [x] Bob receives the confirmation.
- [x] Returning user:
  - [x] Bob visits the platform.
  - [x] Bob can look for more users to send a friend request or visit his friends list.
  - [x] In his friends list, Bob can view status updates.
- [x] Post an Update:
  - [x] Alice decides to update her status.
  - [x] Alice visits the platform and selects the update status option.
  - [x] Alice types her new status and saves it.
  - [x] Bob and all her friends receive a notification that Alice has updated her status.

### Application Overview

- [x] Create a web application that facilitates user connections and real-time interactions.
- [x] The front-end should be built using React, leveraging any state management library.
- [x] The back-end should be implemented in Python using FastAPI.
- [x] Optionally incorporate WebSocket for real-time updates.

### Front-End Development

- [x] Develop the application with React.
- [x] Create personalized user dashboards that show friend lists, incoming requests, and a feed of status updates from friends.

### Back-End Development

- [x] Develop RESTful API endpoints for managing friend requests, user profiles, and status updates.
- [x] Decide on any database and justify the design decision.
- [x] Choose between relational or NoSQL databases and justify the design decision.

### Integration and Communication

- [x] Ensure seamless integration between the front-end and back-end, with a focus on efficient data transfer.
- [x] Handle scenarios where a user receives a friend request or a status update in real-time while they are logged into the application.

### Testing

- Testing is important but not required for this challenge. We will discuss how you would test your app during our next call.

### Documentation and Code Quality

- [x] Ensure code is clean, modular, and adheres to best practices.
- [x] Provide a README file with complete setup and deployment instructions, and detailed API documentation.

### Bonus (Optional)

- [x] Add features like blocking users, reporting inappropriate content, and customizing user privacy settings.

### Submission Guidelines

- [-] Provide all source code via a GitLab or GitHub repository with detailed commit history.
      Detailed commit history is missing as this assesement was done in 3 sitings while in between moving places.
- [x] Document your assumptions.

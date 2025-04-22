workspace {
    name "ArchMessege"
    description "Messenger as a architecture coursework"
    !identifiers hierarchical

    model {
        user = person "User" {
            description "Messenger User"
        }

        user_login_system = softwareSystem "Users System" {

            description "Authentication and adminitration"

            auth_service = container "Auth service" {

                description "Users authentication"
                technology "HTTP, FastApi, PostgreSQL"

            }

            user -> auth_service "Get authorized"
        }

        messenger = softwareSystem "Chat'n Message System" {

            description "PtP and group chat administration"

            messenger_frontend = container "Messenger Frontend System"{

                description "User interface"
                technology "VueJS"
            }

            ptp_chat = container "PtP chat" {

                description "Personal messages"
                technology "WebSocket, WebRTC"
            }

            group_chat = container "Group chat" {

                description "Group messages"
                technology "WebSocket, WebRTC"
            }

            message_service = container "Messages service" {

                description "Message sending and receiving system"
                technology "HTTP, FastApi"
            }

            storage = container "Message Storage" {

                description "Message receiving and saving"
                technology "MongoDB"
            }

            user_login_system -> messenger_frontend "Get access to messnger"
            user -> messenger_frontend "Go to messenger app"
            messenger_frontend -> group_chat "User in group chat"
            messenger_frontend -> ptp_chat "User in PtP chat"
            group_chat -> message_service "Send message"
            ptp_chat -> message_service "Send message"
            message_service -> storage "Write message to database"
            storage -> message_service "Request message from database"
            message_service -> group_chat "Get message from message service"
            message_service -> ptp_chat "Get message from message service"
            messenger_frontend -> user "Get message from messenger"

        }

        notification_system = softwareSystem "Notifications" {

            description "Notification System"

            notification_service = container "Notification Service" {

                description "Send Notification about recived messages"
                technology "HTTPS"
            }

            messenger.message_service -> notification_service "Send Notification about recived messages"
            notification_service -> user "Get Notification"
        }
    }

    views {
        container messenger {

            include *
            autoLayout
            title "Chat system containers"
        }

        systemContext messenger {

            include *
            autoLayout
            title "Chat'n Message system context"
        }

        dynamic messenger  {

            description "Group message sending"
            autoLayout

            user -> user_login_system.auth_service "Login"
            user_login_system.auth_service -> user "Get authorized"
            user -> messenger.messenger_frontend "Send message to group"
            messenger.messenger_frontend -> messenger.group_chat "Publish message in chat"
            messenger.group_chat -> messenger.message_service "Create message"
            messenger.message_service -> messenger.storage "Save message"
            messenger.message_service -> notification_system.notification_service "Send Notification about recived message"
            notification_system.notification_service -> user "Send Notification about unread messages"
        }

        styles {
            element "Element" {
                shape RoundedBox
                background #788B9F
                color #ffffff
            }

            element "Container" {
                shape RoundedBox
                background #51C26A
                color #000000
            }

            element "Person" {
                shape Person
                background  #B7600E
                color #ffffff
            }
        }
    }
}
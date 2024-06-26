import pandas as pd

# Example data

concepts = [
    {
        "unit_number": 1,
        "name": "APIs and Protocols",
        "concepts": {
            "API": "Set of rules that allows different software entities to communicate with each other.",
            "Web API": "An API accessed using HTTP protocol, primarily used by web applications.",
            "RESTful API": "An API that adheres to the constraints of REST architectural style, using standard HTTP methods.",
            "GraphQL": "A query language for APIs that allows clients to request exactly the data they need.",
            "SOAP": "A protocol for exchanging structured information in the implementation of web services.",
            "API Gateway": "A server that acts as an API front-end, receiving API requests and handling them by invoking multiple services."
        }
    },
    {
        "unit_number": 2,
        "name": "Authentication and Security",
        "concepts": {
            "Authorization": "The process of determining if a user has permissions to perform a requested action.",
            "Credentials": "Data used to authenticate or verify a user, typically involving a username and a password.",
            "ID and secret": "A type of credential used to authenticate an entity, often as an API key and secret.",
            "OAuth": "An open standard for access delegation, commonly used as a way to grant websites or applications access to information on other websites.",
            "Token-based authentication": "Security technique where a server generates a token that authorizes the user to access the services.",
            "JWT": "An open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object.",
            "SSL/TLS Encryption": "Protocols for securing communications across a computer network."
        }
    },
    {
        "unit_number": 3,
        "name": "Data Formats and Handling",
        "concepts": {
            "JSON": "A lightweight data-interchange format that is easy for humans to read and write, and for machines to parse and generate.",
            "XML": "A markup language that defines a set of rules for encoding documents in a format that is both human-readable and machine-readable.",
            "data frame": "A two-dimensional, size-mutable, potentially heterogeneous tabular data structure with labeled axes.",
            "Database schemas": "The structure of a database described in a formal language supported by the database management system."
        }
    },
    {
        "unit_number": 4,
        "name": "Networking and Communication",
        "concepts": {
            "cURL": "A command-line tool for getting or sending data using URL syntax.",
            "URL": "Uniform Resource Locator, a reference to a web resource that specifies its location on a computer network.",
            "URI": "Uniform Resource Identifier, a string of characters that unambiguously identifies a particular resource.",
            "http(s)": "HyperText Transfer Protocol (Secure) is the foundation of data communication for the Web.",
            "Webhooks": "User-defined HTTP callbacks that are triggered by specific events, allowing different apps to communicate with each other.",
            "AJAX": "A technique for creating fast and dynamic web pages by making small updates asynchronously.",
            "Middleware": "Software that lies between an operating system and the applications running on it, enabling communication and data management."
        }
    },
    {
        "unit_number": 5,
        "name": "Database Technologies",
        "concepts": {
            "SQL": "A standard language for storing, manipulating, and retrieving data in databases.",
            "NoSQL": "A category of database management systems that does not adhere to the traditional relational database structures."
        }
    },
    {
        "unit_number": 6,
        "name": "Web Development Concepts",
        "concepts": {
            "MVC (Model-View-Controller) Framework": "A pattern used for developing user interfaces that divides an application into three interconnected parts.",
            "CRUD": "An acronym for Create, Read, Update, Delete; basic functions of a database.",
            "Server": "A computer or system that provides resources, data, services, or programs to other computers, known as clients, over a network.",
            "Client": "A piece of computer hardware or software that accesses a service made available by a server.",
            "Status Codes": "Codes issued by a server in response to a client's request made to the server.",
            "Serverless architecture": "An architectural pattern where the server management and capacity planning decisions are abstracted from the developers.",
            "Microservices architecture": "An architectural style that structures an application as a collection of services that are highly maintainable and loosely coupled.",
            "Rate limiting": "A technique used to control the amount of incoming and outgoing traffic to or from a network.",
            "JavaScript":

 "A high-level, dynamic, untyped, and interpreted programming language, standardized in the ECMAScript language specification.",
            "HTML": "The standard markup language used to create web pages.",
            "CSS": "Cascading Style Sheets, a stylesheet language used to describe the presentation of a document written in HTML or XML."
        }
    }
]



# Flatten the data
flattened_data = []
for concept_group in concepts:
    unit_number = concept_group['unit_number']
    unit_name = concept_group['name']
    for concept, definition in concept_group['concepts'].items():
        flattened_data.append({
            "Unit Number": unit_number,
            "Unit Name": unit_name,
            "Concept": concept,
            "Definition": definition
        })

# Convert the flattened data into a DataFrame
df = pd.DataFrame(flattened_data)

# Save the DataFrame to a CSV file
df.to_csv('concepts.csv', index=False)



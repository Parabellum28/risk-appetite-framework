import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="risk_docs")

docs = [
    "High-risk assets require strong security controls such as encryption, strict access control, continuous monitoring, and regular audits to prevent breaches.",
    "Low-risk systems can be managed with standard monitoring, periodic audits, and basic security practices without heavy controls.",
    "Critical risks require immediate remediation, real-time monitoring, and incident response to prevent system failure or data loss.",
    "Vulnerabilities should be identified through scans and patched quickly to reduce the risk of exploitation.",
    "Risk appetite defines the acceptable level of risk an organization is willing to take in its operations.",
    "Access control ensures only authorized users can access systems, reducing the chance of unauthorized activity.",
    "Data encryption protects sensitive information both at rest and in transit from unauthorized access.",
    "Incident response plans help organizations quickly detect, respond to, and recover from security incidents.",
    "Regular security audits help identify weaknesses and improve overall system security posture.",
    "Compliance ensures that systems follow required regulations and standards such as ISO or GDPR."
]

# Avoid duplicate insert
if collection.count() == 0:
    collection.add(
        documents=docs,
        ids=[str(i) for i in range(len(docs))]
    )
    print("✅ Data seeded")

# Query
results = collection.query(
    query_texts=["What applies to high-risk assets?"],
    n_results=2
)

print("\n🔍 Results:")
for doc in results["documents"][0]:
    print("-", doc)
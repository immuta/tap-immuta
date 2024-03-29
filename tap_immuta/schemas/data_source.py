from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("name", th.StringType),
    th.Property("recordFormat", th.StringType),
    th.Property("description", th.StringType),
    th.Property("policyHandler", th.ObjectType()),
    th.Property("sqlSchemaName", th.StringType),
    th.Property("sqlTableName", th.StringType),
    th.Property("blobHandler", th.ObjectType()),
    th.Property("createdBy", th.IntegerType),
    th.Property("deleted", th.BooleanType),
    th.Property("type", th.StringType),
    th.Property("recordCount", th.IntegerType),
    th.Property("rowCount", th.IntegerType),
    th.Property("documentation", th.StringType),
    th.Property("statsExpiration", th.StringType),
    th.Property("id", th.IntegerType),
    th.Property("blobHandlerType", th.StringType),
    th.Property("policyHandlerType", th.StringType),
    th.Property("subscriptionType", th.StringType),
    th.Property("subscriptionPolicy", th.ObjectType()),
    th.Property("globalPolicies", th.ArrayType(th.ObjectType())),
    th.Property("status", th.StringType),
    th.Property("statusInfo", th.ObjectType()),
    th.Property("expiration", th.StringType),
    th.Property("catalogMetadata", th.StringType),
    th.Property("workspace", th.StringType),
    th.Property("seeded", th.BooleanType),
    th.Property("schemaEvolutionId", th.IntegerType),
    th.Property("connectionString", th.StringType),
    th.Property("columnEvolutionEnabled", th.BooleanType),
    th.Property("createdAt", th.StringType),
    th.Property("updatedAt", th.StringType),
    th.Property("subscribedAsUser", th.BooleanType),
    th.Property("subscriptionId", th.IntegerType),
    th.Property("acknowledgeRequired", th.BooleanType),
    th.Property("subscriptionStatus", th.StringType),
    th.Property("requestedState", th.StringType),
    th.Property("approved", th.BooleanType),
    th.Property("subscriptionExpiration", th.StringType),
    th.Property("filterId", th.StringType),
    th.Property("subscribers", th.StringType),
    th.Property("tags", th.ArrayType(th.StringType)),
    th.Property("fingerprintCreatedAt", th.DateTimeType),
    th.Property("schemaEvolution", th.ObjectType()),
).to_dict()

from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("id", th.IntegerType),
    th.Property("projectKey", th.StringType),
    th.Property("name", th.StringType),
    th.Property("status", th.StringType),
    th.Property("description", th.StringType),
    th.Property("documentation", th.StringType),
    th.Property("deleted", th.BooleanType),
    th.Property("allowMaskedJoins", th.BooleanType),
    th.Property("subscriptionType", th.StringType),
    th.Property("subscriptionPolicy", th.ObjectType()),
    th.Property("equalization", th.ObjectType(
        th.Property("setNone", th.BooleanType),
        th.Property("createdAt", th.StringType),
        th.Property("recommended", th.StringType),
        th.Property("validationFrequency", th.IntegerType),
        th.Property("authsForPolicyHandler", th.ObjectType(
            th.Property("groups", th.ArrayType(th.StringType)),
            th.Property("authorizations", th.ObjectType()),
        )),
    )),
    th.Property("workspace", th.ObjectType()),
    th.Property("snowflake", th.ObjectType()),
    th.Property("createdBy", th.IntegerType),
    th.Property("updatedBy", th.IntegerType),
    th.Property("createdAt", th.StringType),
    th.Property("updatedAt", th.StringType),
    th.Property("subscribedAsUser", th.BooleanType),
    th.Property("subscriptionId", th.IntegerType),
    th.Property("acknowledgeRequired", th.BooleanType),
    th.Property("subscriptionStatus", th.StringType),
    th.Property("requestedState", th.StringType),
    th.Property("approved", th.BooleanType),
    th.Property("subscriptionExpiration", th.StringType),
    th.Property("filterId", th.IntegerType),
    th.Property("purposeCount", th.IntegerType),
    th.Property("hasSqlAccount", th.BooleanType),
    th.Property("purposes", th.ArrayType(th.StringType)),
    th.Property("stagedPurposes", th.ArrayType(th.StringType)),
    th.Property("tags", th.ArrayType(th.StringType)),
).to_dict()

from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("project_id", th.IntegerType),
    th.Property("profile", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("iamid", th.StringType),
    th.Property("userid", th.StringType),
    th.Property("email", th.StringType),
    th.Property("type", th.StringType),
    th.Property("approved", th.BooleanType),
    th.Property("state", th.StringType),
    th.Property("systemGenerated", th.BooleanType),
    th.Property("lastExternalRefresh", th.StringType),
    th.Property("subscriptionId", th.IntegerType),
    th.Property("createdAt", th.StringType),
    th.Property("updatedAt", th.StringType),
    th.Property("approvals", th.ArrayType(th.StringType)),
    th.Property("currentUserCanApprove", th.BooleanType),
    th.Property(
        "compliance",
        th.ObjectType(
            th.Property("isMissingPurposeAcknowledgement", th.BooleanType),
            th.Property("validationFrequencyExceeded", th.BooleanType),
            th.Property("isMissingEntitlements", th.BooleanType),
            th.Property("invalidSubscriptions", th.ArrayType(th.StringType)),
            th.Property("missingDataSources", th.ArrayType(th.StringType)),
        ),
    ),
).to_dict()

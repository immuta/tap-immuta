from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("project_id", th.IntegerType),
    th.Property("addedBy", th.StringType),
    th.Property("dataSourceName", th.StringType),
    th.Property("policyHandlerType", th.StringType),
    th.Property("addedOn", th.StringType),
    th.Property("dataSourceId", th.IntegerType),
    th.Property("addedByProfile", th.IntegerType),
    th.Property("comment", th.StringType),
    th.Property("deleted", th.BooleanType),
    th.Property("subscriptionType", th.StringType),
    th.Property("subscriptionStatus", th.StringType),
    th.Property("subscriptionPolicy", th.ObjectType()),
    th.Property("connectionString", th.StringType),
    th.Property("blobHandlerType", th.StringType),
    th.Property("derivedInThisProject", th.BooleanType),
).to_dict()

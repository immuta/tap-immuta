from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("data_source_id", th.IntegerType),
    th.Property("profile", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("iamid", th.StringType),
    th.Property("userid", th.StringType),
    th.Property("email", th.StringType),
    th.Property("admin", th.StringType),
    th.Property("approved", th.BooleanType),
    th.Property("state", th.StringType),
    th.Property("systemGenerated", th.BooleanType),
    th.Property("lastExternalRefresh", th.StringType),
    th.Property("subscriptionId", th.IntegerType),
    th.Property("createdAt", th.StringType),
    th.Property("updatedAt", th.StringType),
    th.Property("approvals", th.ArrayType(th.StringType)),
).to_dict()

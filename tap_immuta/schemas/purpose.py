from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("id", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("acknowledgement", th.StringType),
    th.Property("description", th.StringType),
    th.Property("addedByProfile", th.IntegerType),
    th.Property("displayAcknowledgement", th.BooleanType),
    th.Property("deleted", th.BooleanType),
    th.Property("systemGenerated", th.BooleanType),
    th.Property("createdAt", th.StringType),
    th.Property("updatedAt", th.StringType),
).to_dict()

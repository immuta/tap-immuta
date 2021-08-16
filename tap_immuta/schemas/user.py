from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("authentication", th.IntegerType),
    th.Property("createdAt", th.StringType),
    th.Property("disabled", th.BooleanType),
    th.Property("iamid", th.StringType),
    th.Property("id", th.IntegerType),
    th.Property("lastExternalRefresh", th.StringType),
    th.Property("systemGenerated", th.BooleanType),
    th.Property("updatedAt", th.StringType),
    th.Property("userid", th.StringType),
    th.Property("permissions", th.ArrayType(th.StringType)),
    th.Property("profile", th.ObjectType(
        th.Property("createdAt", th.StringType),
        th.Property("email", th.StringType),
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("systemGenerated", th.BooleanType),
        th.Property("updatedAt", th.StringType),
    )),
).to_dict()

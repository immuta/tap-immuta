from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("id", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("type", th.StringType),
    th.Property("template", th.BooleanType),
    th.Property("staged", th.BooleanType),
    th.Property("systemGenerated", th.BooleanType),
    th.Property("deleted", th.BooleanType),
    th.Property("createdBy", th.IntegerType),
    th.Property("createdByName", th.StringType),
    th.Property("createdAt", th.StringType),
    th.Property("updatedAt", th.StringType),
    th.Property("certification", th.ObjectType(
        th.Property("text", th.StringType),
        th.Property("label", th.StringType),
        th.Property("tags", th.ArrayType(th.StringType)),
    )),
    th.Property("actions", th.ArrayType(
        th.ObjectType(
            th.Property("type", th.StringType),
            th.Property("rules", th.ObjectType(
                th.Property("type", th.StringType),
            )),
            th.Property("description", th.StringType),
        )),
    ),
).to_dict()

# TEMP


FROM microsoft/dotnet:2.1-runtime AS base
WORKDIR /app

FROM microsoft/dotnet:2.1-sdk AS build
WORKDIR /src
COPY MQTT_Client/MQTT_Client.csproj MQTT_Client/
RUN dotnet restore MQTT_Client/MQTT_Client.csproj
COPY . .
WORKDIR /src/MQTT_Client
RUN dotnet build MQTT_Client.csproj -c Release -o /app

FROM build AS publish
RUN dotnet publish MQTT_Client.csproj -c Release -o /app

FROM base AS final
WORKDIR /app
COPY --from=publish /app .
ENTRYPOINT ["dotnet", "MQTT_Client.dll"]

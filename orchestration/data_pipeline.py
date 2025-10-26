from prefect import flow, task
from ingestion.get_and_write_raw_data import get_data, write_eia_to_postgresql, write_nhl_to_postgresql
from reports.create_report import create_report
import httpx
from prefect_dbt.cli.commands import DbtCoreOperation


@task(name="retrieving api nhl data")
async def call_fastapi():
    url = "http://host.docker.internal:8000/nhl-data"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data_list_of_dict = response.text
        return data_list_of_dict

@task(name="retrieving main eia data")
async def fetch_eia_data():
    data = get_data()
    return data

@task(name="storing raw main eia in database")
async def store_data_eia(data):
    write_eia_to_postgresql(data)

@task(name="storing raw nhl teams in database")
async def store_data_nhl(data):
    write_nhl_to_postgresql(data)

@task(name="run dbt silver")
def run_dbt_silver():
    DbtCoreOperation(
        commands=["dbt run --models silver"],
        project_dir="/app/dbt",
        profiles_dir="/app/dbt"
    ).run()

@task(name="run dbt gold")
def run_dbt_gold():
    DbtCoreOperation(
        commands=["dbt run --models gold"],
        project_dir="/app/dbt",
        profiles_dir="/app/dbt"
    ).run()

@task(name="creating report")
def create_report_prefect():
    create_report()

@flow(name="Local Data Pipeline")
async def data_pipeline():
    print("running full pipeline.......")

    print("getting nhl data...")
    nhl_data = await call_fastapi()
    print("storing nhl data..")
    await store_data_nhl(nhl_data)

    print("getting eia data...")
    data = await fetch_eia_data()
    print("storing eia data...")
    await store_data_eia(data)

    print("running dbt silver...")
    run_dbt_silver()

    print("running dbt gold...")
    run_dbt_gold()
    print("data pipeline is complete!")

    print("creating report...")
    create_report_prefect()


if __name__ == "__main__":
    import asyncio
    asyncio.run(data_pipeline())


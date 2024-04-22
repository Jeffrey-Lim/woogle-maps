"""Computes the x and y coordinates for the nodes in the graph, based on a story that each row is in."""

import math
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal, override

import pandas as pd
import polars as pl
from epochalyst.pipeline.model.transformation.transformation_block import TransformationBlock

from src.logging.logger import Logger


@dataclass
class ComputeLayout(TransformationBlock, Logger):
    """Compute the layout of the graph.

    The data is expected to have "adj_list", "adj_weights" columns that contains the adjacency list of the graph.
    The "storyline" column contains the storyline index for each row.
    It will return the data with "x" and "y" columns that contains the layout for each row.

    :param spacing_within_story: The spacing of the nodes. Either "uniform" or "time-scaled".
    :param transpose: Transpose the x and y coordinates.
    """

    spacing_within_story: Literal["uniform", "time-scaled"] = "uniform"
    transpose: bool = False

    @override
    def custom_transform(self, data: pd.DataFrame | pl.DataFrame, **transform_args: Any) -> pd.DataFrame:  # noqa: DOC103  # type: ignore[misc]
        """Compute the layout of the graph.

        Retrieves the storylines from the data and computes the layout of the nodes.

        :param data: The data to compute the layout for.
        :param transform_args: Additional keyword arguments (UNUSED).
        :return: The data with the layout.
        """
        if "adj_list" not in data.columns or "adj_weights" not in data.columns or "storyline" not in data.columns:
            self.log_to_warning("The data does not contain valid 'adj_list', 'adj_weights', and/or storyline' columns. Not computing layout.")
            return data

        if isinstance(data, pd.DataFrame):
            data = pl.from_pandas(data)

        full_data = None
        if "clusters" in data.columns:
            full_data = data.clone().drop(["adj_list", "adj_weights", "storyline"])
            data = (
                data.group_by("clusters")
                .agg(
                    [
                        pl.col("adj_list").first().alias("adj_list"),
                        pl.col("adj_weights").first().alias("adj_weights"),
                        pl.col("storyline").first().alias("storyline"),
                        pl.col("date").median().alias("date"),
                    ],
                )
                .sort("clusters")
            )

        self.log_to_terminal(f"Computing layout of {data.height} nodes...")

        # Group data by storyline and get nodes within each storyline
        storylines: pl.DataFrame = data.select("storyline").with_row_index().group_by("storyline").agg(pl.col("index")).sort("storyline")

        if self.spacing_within_story == "time-scaled":
            if ("date" not in data.columns) or (data["date"].max() is None) or (data["date"].min() == data["date"].max()):
                self.log_to_warning("The data does not contain a valid 'date' column. Uniform node spacing is forced.")
                self.spacing_within_story = "uniform"
            else:
                min_date: datetime = data["date"].min()
                max_date: datetime = data["date"].max()
                total_range_seconds = (max_date - min_date).total_seconds()
                node_dates: list[datetime] = data["date"].to_list()

        x_coords = [0.0] * data.height
        y_coords = [0.0] * data.height

        max_story_length: int = storylines["index"].list.len().max()

        for story_id, node_indices in storylines.iter_rows():
            y = math.ceil(story_id / 2) * ((-1) ** story_id) * 200  # Make storylines alternate between top and bottom of the main storyline

            for i, node_index in enumerate(node_indices):
                if self.spacing_within_story == "time-scaled":
                    timeline_position = (node_dates[node_index] - min_date).total_seconds() / total_range_seconds
                    x = timeline_position * max_story_length * 150
                else:
                    x = i * max_story_length * 15

                x_coords[node_index] = x
                y_coords[node_index] = y

        if self.transpose:  # Swap x and y coordinates
            x_coords, y_coords = y_coords, x_coords

        data = data.with_columns(
            [
                pl.Series("x", x_coords),
                pl.Series("y", y_coords),
            ],
        ).drop("index")

        if full_data is not None:
            data = data.drop("date").join(full_data, on="clusters")

        return data.to_pandas().drop("index", errors="ignore")

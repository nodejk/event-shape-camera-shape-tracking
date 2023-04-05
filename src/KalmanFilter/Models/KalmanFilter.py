import typing
import numpy
from stonesoup.models.transition.linear import (
    CombinedLinearGaussianTransitionModel,
    ConstantVelocity,
    RandomWalk,
    ConstantNthDerivative,
)
from stonesoup.hypothesiser.distance import DistanceHypothesiser
from stonesoup.measures import Mahalanobis
from stonesoup.models.measurement.linear import LinearGaussian
from stonesoup.predictor.kalman import KalmanPredictor
from stonesoup.reader import DetectionReader
from stonesoup.updater.kalman import KalmanUpdater
from stonesoup.types.state import GaussianState
from stonesoup.types.array import CovarianceMatrix, StateVector
from stonesoup.initiator.simple import MultiMeasurementInitiator
from stonesoup.deleter.time import UpdateTimeStepsDeleter
from stonesoup.dataassociator.neighbour import GNNWith2DAssignment
from stonesoup.tracker.simple import MultiTargetTracker


class KalmanFilter:
    tracker: MultiTargetTracker

    def __init__(self, detector: DetectionReader) -> None:
        transition_model = CombinedLinearGaussianTransitionModel(
            KalmanFilter.get_transition_models()
        )
        measurement_model = LinearGaussian(
            **KalmanFilter.get_measurement_model_properties()
        )

        predictor: KalmanPredictor = KalmanPredictor(transition_model)
        updater: KalmanUpdater = KalmanUpdater(measurement_model)

        hypothesiser = DistanceHypothesiser(predictor, updater, Mahalanobis(), 10)

        prior_state = GaussianState(
            StateVector(numpy.zeros((6, 1))),
            CovarianceMatrix(
                numpy.diag([100**2, 30**2, 100**2, 30**2, 100**2, 100**2])
            ),
        )

        deleter_init = UpdateTimeStepsDeleter(time_steps_since_update=3)

        data_associator = GNNWith2DAssignment(hypothesiser)

        initiator = MultiMeasurementInitiator(
            prior_state,
            deleter_init,
            data_associator,
            updater,
            measurement_model,
            min_points=10,
        )

        deleter = UpdateTimeStepsDeleter(time_steps_since_update=15)

        self.tracker = MultiTargetTracker(
            initiator=initiator,
            detector=detector,
            deleter=deleter,
            data_associator=data_associator,
            updater=updater,
        )

    @staticmethod
    def get_transition_models() -> typing.List[ConstantNthDerivative]:
        return [
            ConstantVelocity(20**2),
            ConstantVelocity(20**2),
            RandomWalk(20**2),
            RandomWalk(20**2),
        ]

    @staticmethod
    def get_measurement_model_properties() -> typing.Dict:
        return {
            "ndim_state": 6,
            "mapping": [0, 2, 4, 5],
            "noise_covar": numpy.diag([1**2, 1**2, 3**2, 3**2]),
        }

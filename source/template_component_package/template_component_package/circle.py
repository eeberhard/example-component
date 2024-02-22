from modulo_components.lifecycle_component import LifecycleComponent
import state_representation as sr
import numpy as np
from modulo_core.encoded_state import EncodedState
from clproto.MessageType import CARTESIAN_POSE_MESSAGE


class Circle(LifecycleComponent):
    def __init__(self, node_name: str, *args, **kwargs):
        super().__init__(node_name, *args, **kwargs)
        # add parameters, inputs and outputs here

        self._tf_name = sr.Parameter("tf_name", "circle", sr.ParameterType.STRING)
        self.add_parameter("_tf_name", "The name of the TF to broadcaster")

        self.add_tf_broadcaster()

        self._circle_pose = sr.CartesianPose()
        self.add_output("circle_pose", "_circle_pose", EncodedState, CARTESIAN_POSE_MESSAGE)

        self._time_factor = 0

    def on_validate_parameter_callback(self, parameter: sr.Parameter) -> bool:
        # validate an incoming parameter value according to some criteria
        if parameter.get_name() == "tf_name":
            if len(parameter.get_value()) < 3:
                self.get_logger().error(f"Cannot set TF name with less than three characters ({parameter.get_value()})")
                return False
        return True

    def on_configure_callback(self) -> bool:
        # configuration steps before activation

        self.get_logger().info("Configuring my component!")

        self._circle_pose.set_name(self._tf_name.get_value())
        self._circle_pose.set_position(0.0, 0.0, 0.0)

        return True

    def on_activate_callback(self) -> bool:
        self.get_logger().info("Activating my component!")
        # activation steps before running
        return True

    def on_deactivate_callback(self) -> bool:
        # deactivation steps
        return True

    def on_step_callback(self):
        # do something periodically

        self._time_factor += 1.0 / self.get_parameter_value("rate")

        self._circle_pose.set_position(np.cos(self._time_factor), np.sin(self._time_factor), 0.0)
        self.get_logger().info(f"{self._circle_pose}", throttle_duration_sec=0.1)

        self.send_transform(self._circle_pose)

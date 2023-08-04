#include <pybind11/pybind11.h>
#include "libMTSClient.h"
#include "libMTSMaster.h"

namespace py = pybind11;

struct MTSClientWrapper {
    MTSClient *ptr;
};

MTSClientWrapper register_client(){
    MTSClient* m = MTS_RegisterClient();
    return MTSClientWrapper{m};
}

void deregister_client(MTSClientWrapper client){
    MTS_DeregisterClient(client.ptr);
}

double note_to_frequency(MTSClientWrapper client, int midinote, int midichannel){
    return MTS_NoteToFrequency(client.ptr, midinote, midichannel);
}

double retuning_in_semitones(MTSClientWrapper client, int midinote, int midichannel){
    return MTS_RetuningInSemitones(client.ptr, midinote, midichannel);
}

double retuning_as_ratio(MTSClientWrapper client, int midinote, int midichannel){
    return MTS_RetuningAsRatio(client.ptr, midinote, midichannel);
}

void set_note_tuning(float frequency_in_hz, int midinote){
    MTS_SetNoteTuning(frequency_in_hz, midinote);
}

PYBIND11_MODULE(mtsespy, m)
{
    m.doc() = "Wrapper for ODDSound MTS-ESP C++ library";
    py::class_<MTSClientWrapper>(m, "MTSClient");
    m.def("register_client", &register_client, "Register MTS client");
    m.def("deregister_client", &deregister_client, "De-register MTS client");
    m.def("note_to_frequency", &note_to_frequency, "Convert midi note to frequency");
    m.def("retuning_in_semitones", &retuning_in_semitones, "Midi note retuning in semitones");
    m.def("retuning_as_ratio", &retuning_as_ratio, "Midi note retuning as ratio");
    m.def("can_register_master", &MTS_CanRegisterMaster, "Check if master has already been registered");
    m.def("register_master", &MTS_RegisterMaster, "Register MTS master");
    m.def("deregister_master", &MTS_DeregisterMaster, "Deregister MTS master");
    m.def("set_note_tuning", &set_note_tuning, "Set tuning of single note");
}

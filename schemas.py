from datetime import timezone as dt_timezone
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

def _utc_now_iso() -> str:
    return datetime.now(dt_timezone.utc).isoformat().replace('+00:00', 'Z')

class HealthResponse(BaseModel):
    status: str = Field(default='healthy', description='Service health status')
    timestamp: str = Field(default_factory=_utc_now_iso, description='UTC timestamp in ISO-8601 format')

class ToolItem(BaseModel):
    name: str = Field(default='', description='Tool identifier')
    description: str = Field(default='', description='Tool capabilities')
    input_schema: Dict[str, Any] = Field(default_factory=dict, description='JSON Schema for inputs')

class ToolsResponse(BaseModel):
    tools: List[Dict[str, Any]] = Field(default_factory=list, description='Registered agent tools list')

class ExplainabilityMetrics(BaseModel):
    primary_driver: str = Field(default='sky_visibility', description='Primary contributing analytical factor')
    weights: Dict[str, float] = Field(default_factory=lambda: {'visibility': 0.3, 'space_weather': 0.3, 'orbital_activity': 0.2, 'cosmic_events': 0.2}, description='Weighting coefficients used in computation')

class ComputeSkyIntelligenceRequest(BaseModel):
    target_identifier: str = Field(default='sky_global', description='Target identifier or spatial zone')
    query_parameter: str = Field(default='full_sky_analysis', description='Specific analysis mode or query parameter')
    lat: float = Field(default=2.27, description='Latitude in decimal degrees [-90, 90]')
    lon: float = Field(default=102.55, description='Longitude in decimal degrees [-180, 180]')
    altitude_m: float = Field(default=20.0, description='Observer altitude in meters above sea level')
    lookahead_hours: int = Field(default=72, description='Prediction lookahead window in hours')
    window_steps: int = Field(default=24, description='Number of temporal resolution steps')
    resolution: int = Field(default=8, description='Spatial H3 resolution index')

class ComputeSkyIntelligenceResponse(BaseModel):
    timestamp: str = Field(default_factory=_utc_now_iso, description='UTC computation timestamp')
    status: str = Field(default='healthy', description='Computation status')
    primary_metric: float = Field(default=88.2, description='Primary metric score (e.g., Sky Intelligence Score 0-100)')
    secondary_score: float = Field(default=0.93, description='Normalized secondary confidence or ratio index')
    state_index: float = Field(default=84.7, description='Aggregated readiness or risk state index')
    classification: str = Field(default='OBSERVATORY_GRADE', description='State classification category')
    explainability: ExplainabilityMetrics = Field(default_factory=ExplainabilityMetrics, description='Decomposition and factor weights')

class GetSpatialH3TensorRequest(BaseModel):
    lat: float = Field(default=2.0442, description='Latitude in decimal degrees [-90, 90]')
    lon: float = Field(default=102.5689, description='Longitude in decimal degrees [-180, 180]')
    resolution: int = Field(default=8, description='H3 spatial resolution [7, 8, 9]')
    lookahead_hours: int = Field(default=24, description='Lookahead window for spatial aggregation')

class GetSpatialH3TensorResponse(BaseModel):
    h3_index: str = Field(default='886520d81dfffff', description='H3 spatial index cell string')
    spatial_cell: str = Field(default='886520d81dfffff', description='Duplicated H3 index reference')
    density_score: float = Field(default=64.2, description='Aggregated sky/orbital density score (0-100)')
    terrain_state_index: float = Field(default=75.1, description='Regional observability or environment readiness score')
    status: str = Field(default='ACTIVE', description='Cell operational activity state')

class PredictSatellitePassesRequest(BaseModel):
    lat: float = Field(default=2.27, description='Observer latitude')
    lon: float = Field(default=102.55, description='Observer longitude')
    altitude_m: float = Field(default=20.0, description='Observer altitude in meters')
    min_elevation_deg: float = Field(default=10.0, description='Minimum pass elevation threshold in degrees')
    lookahead_hours: int = Field(default=24, description='Prediction window in hours')

class PredictSatellitePassesResponse(BaseModel):
    timestamp: str = Field(default_factory=_utc_now_iso, description='Execution timestamp')
    status: str = Field(default='success', description='Execution status')
    passes_detected: int = Field(default=14, description='Number of qualifying satellite passes')
    pass_schedule: List[Dict[str, Any]] = Field(default_factory=list, description='Detailed pass ephemerides')

class ComputeSpaceWeatherRiskRequest(BaseModel):
    solar_flux: float = Field(default=150.0, description='Solar radio flux index (F10.7)')
    proton_flux: float = Field(default=1.5, description='High energy proton flux measurement')
    kp_index: float = Field(default=3.0, description='Geomagnetic Kp index (0-9)')

class ComputeSpaceWeatherRiskResponse(BaseModel):
    timestamp: str = Field(default_factory=_utc_now_iso, description='Execution timestamp')
    risk_score: float = Field(default=35.0, description='Normalized geomagnetic/space weather risk (0-100)')
    classification: str = Field(default='ACTIVE', description='Space weather classification state')
    swi: float = Field(default=0.45, description='Space Weather Index (SWI)')

class ComputeOrbitalCongestionRequest(BaseModel):
    lat: float = Field(default=0.0, description='Target center latitude')
    lon: float = Field(default=0.0, description='Target center longitude')
    radius_km: float = Field(default=500.0, description='Spatial sampling radius in kilometers')

class ComputeOrbitalCongestionResponse(BaseModel):
    timestamp: str = Field(default_factory=_utc_now_iso, description='Execution timestamp')
    satellite_density: float = Field(default=12.4, description='Satellites per orbital shell / area unit')
    oai: float = Field(default=55.0, description='Orbital Activity Index (OAI)')
    classification: str = Field(default='MODERATE', description='Congestion classification state')

class ComputeDarkSkyScoreRequest(BaseModel):
    lat: float = Field(default=2.27, description='Observer latitude')
    lon: float = Field(default=102.55, description='Observer longitude')
    light_pollution_nadir: float = Field(default=12.5, description='Nadir radiance or light pollution value')

class ComputeDarkSkyScoreResponse(BaseModel):
    timestamp: str = Field(default_factory=_utc_now_iso, description='Execution timestamp')
    darkness_score: float = Field(default=0.78, description='Darkness quality index (0-1)')
    svi: float = Field(default=74.5, description='Sky Visibility Index (SVI)')

class ComputeAuroraProbabilityRequest(BaseModel):
    lat: float = Field(default=65.0, description='Observer latitude')
    kp_index: float = Field(default=6.0, description='Geomagnetic Kp index (0-9)')

class ComputeAuroraProbabilityResponse(BaseModel):
    timestamp: str = Field(default_factory=_utc_now_iso, description='Execution timestamp')
    aurora_score: float = Field(default=0.67, description='Normalized aurora potential score (0-1)')
    classification: str = Field(default='STORM', description='Auroral activity classification')

class ComputeMeteorVisibilityRequest(BaseModel):
    zenith_hourly_rate: float = Field(default=120.0, description='Current shower ZHR')
    peak_rate: float = Field(default=150.0, description='Maximum historical or expected peak ZHR')
    radiant_altitude_deg: float = Field(default=45.0, description='Radiant elevation angle')

class ComputeMeteorVisibilityResponse(BaseModel):
    timestamp: str = Field(default_factory=_utc_now_iso, description='Execution timestamp')
    intensity: float = Field(default=0.8, description='Normalized meteor intensity index (0-1)')
    status: str = Field(default='ACTIVE', description='Meteor shower activity status')

class ComputeNeoRiskRequest(BaseModel):
    distance_au: float = Field(default=0.05, description='Closest approach distance in Astronomical Units')
    size_factor: float = Field(default=1.2, description='Estimated diameter or mass scaling factor')

class ComputeNeoRiskResponse(BaseModel):
    timestamp: str = Field(default_factory=_utc_now_iso, description='Execution timestamp')
    proximity_score: float = Field(default=20.0, description='Inverse distance proximity factor')
    neo_risk: float = Field(default=24.0, description='Computed NEO risk metric')
    classification: str = Field(default='ELEVATED', description='Risk tier classification')

class ComputeObservabilityIndexRequest(BaseModel):
    svi: float = Field(default=80.0, description='Sky Visibility Index')
    darkness: float = Field(default=0.85, description='Darkness rating')
    weather_suitability: float = Field(default=0.9, description='Weather suitability factor')

class ComputeObservabilityIndexResponse(BaseModel):
    timestamp: str = Field(default_factory=_utc_now_iso, description='Execution timestamp')
    ori: float = Field(default=84.5, description='Observatory Readiness Index (ORI)')
    classification: str = Field(default='OBSERVATORY_GRADE', description='Readiness classification state')

class DetectCosmicEventsRequest(BaseModel):
    lookahead_hours: int = Field(default=72, description='Event scan lookahead window')

class DetectCosmicEventsResponse(BaseModel):
    timestamp: str = Field(default_factory=_utc_now_iso, description='Execution timestamp')
    events_detected: int = Field(default=5, description='Count of transient or recurring cosmic events')
    event_catalog: List[Dict[str, Any]] = Field(default_factory=list, description='Catalog of detected transient events')

class RankCelestialTargetsRequest(BaseModel):
    targets: List[str] = Field(default_factory=lambda: ['Sirius', 'Betelgeuse', 'Andromeda Galaxy'], description='Celestial object identifiers')
    lat: float = Field(default=2.27, description='Observer latitude')
    lon: float = Field(default=102.55, description='Observer longitude')

class RankCelestialTargetsResponse(BaseModel):
    timestamp: str = Field(default_factory=_utc_now_iso, description='Execution timestamp')
    ranked_targets: List[Dict[str, Any]] = Field(default_factory=list, description='Ordered targets by CEPI priority')

class ForecastSkyConditionsRequest(BaseModel):
    lat: float = Field(default=2.27, description='Observer latitude')
    lon: float = Field(default=102.55, description='Observer longitude')
    horizon_hours: int = Field(default=24, description='Forecast horizon in hours')

class ForecastSkyConditionsResponse(BaseModel):
    timestamp: str = Field(default_factory=_utc_now_iso, description='Execution timestamp')
    forecast_steps: List[Dict[str, Any]] = Field(default_factory=list, description='Time-series forecast items')